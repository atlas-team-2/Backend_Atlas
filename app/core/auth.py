import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

from app.core.settings import settings
from app.dependencies.services import RefreshSessionServiceDep, UserServiceDep
from app.models.entities.refresh_session import RefreshSessionCreate
from app.models.entities.user import User
from app.schemas.auth import AuthData, AuthTokenData
from app.utils.hasher import Hasher


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()


def _b64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


class Authenticator:
    def __init__(
        self,
        user_service: UserServiceDep,
        refresh_session_service: RefreshSessionServiceDep,
    ):
        self.__user_service = user_service
        self.__refresh_session_service = refresh_session_service

    def __create_user_token(
        self,
        user_id: UUID,
        token_id: UUID,
        expires_at: datetime,
    ) -> str:
        if settings.auth.algorithm != 'HS256':
            msg = 'Only HS256 algorithm is supported'
            raise ValueError(msg)

        payload = {
            'sub': str(user_id),
            'exp': int(expires_at.timestamp()),
            'jti': str(token_id),
            'iat': int(datetime.now(timezone.utc).timestamp()),
        }
        header = {
            'alg': settings.auth.algorithm,
            'typ': 'JWT',
        }

        signing_input = '.'.join(
            [
                _b64url_encode(json.dumps(header).encode()),
                _b64url_encode(json.dumps(payload).encode()),
            ],
        )
        signature = hmac.new(
            settings.auth.secret.get_secret_value().encode(),
            signing_input.encode(),
            hashlib.sha256,
        ).digest()
        return f'{signing_input}.{_b64url_encode(signature)}'

    def __decode_token(self, token: str) -> dict:
        if settings.auth.algorithm != 'HS256':
            msg = 'Only HS256 algorithm is supported'
            raise ValueError(msg)

        try:
            header_part, payload_part, signature_part = token.split('.')
        except ValueError as exc:
            msg = 'Invalid token format'
            raise ValueError(msg) from exc

        signing_input = f'{header_part}.{payload_part}'
        expected_signature = hmac.new(
            settings.auth.secret.get_secret_value().encode(),
            signing_input.encode(),
            hashlib.sha256,
        ).digest()
        actual_signature = _b64url_decode(signature_part)

        if not hmac.compare_digest(expected_signature, actual_signature):
            msg = 'Invalid token signature'
            raise ValueError(msg)

        payload = json.loads(_b64url_decode(payload_part))
        expires_at = payload.get('exp', 0)
        now = datetime.now(timezone.utc).timestamp()
        if now > expires_at:
            msg = 'Token has expired'
            raise ValueError(msg)

        return payload

    async def __get_user_token_data(
        self,
        token: str,
    ) -> Optional[tuple[User, UUID]]:
        try:
            decoded_payload = self.__decode_token(token)
            raw_user_id = decoded_payload.get('sub')
            raw_token_id = decoded_payload.get('jti')

            user_id = UUID(raw_user_id)
            token_id = UUID(raw_token_id)
        except (TypeError, ValueError):
            return None

        user = await self.__user_service.get_user(user_id)
        if user is None:
            return None

        return user, token_id

    async def authenticate_user(self, access_token: str) -> Optional[User]:
        token_data = await self.__get_user_token_data(access_token)
        if token_data is None:
            return None

        user, access_token_id = token_data
        refresh_service = self.__refresh_session_service
        user_active_session = await refresh_service.get_active_user_session(user.id)
        if user_active_session is None:
            return None

        if user_active_session.access_token_id != access_token_id:
            return None

        return user

    async def __generate_tokens(self, user_id: UUID) -> Optional[AuthTokenData]:
        has_active_sessions = (
            await self.__refresh_session_service.has_user_active_session(user_id)
        )
        if has_active_sessions:
            return None

        now = datetime.now(timezone.utc)

        access_token_id = uuid4()
        access_token_lifetime_timedelta = timedelta(
            seconds=settings.auth.access_token_lifetime_seconds,
        )
        access_token_expires_at = now + access_token_lifetime_timedelta
        access_token = self.__create_user_token(
            user_id=user_id,
            token_id=access_token_id,
            expires_at=access_token_expires_at,
        )

        refresh_token_id = uuid4()
        refresh_token_lifetime_timedelta = timedelta(
            seconds=settings.auth.refresh_token_lifetime_seconds,
        )
        refresh_token_expires_at = now + refresh_token_lifetime_timedelta
        refresh_token = self.__create_user_token(
            user_id=user_id,
            token_id=refresh_token_id,
            expires_at=refresh_token_expires_at,
        )

        session_create_data = RefreshSessionCreate(
            user_id=user_id,
            access_token_id=access_token_id,
            refresh_token_id=refresh_token_id,
            expires_at=refresh_token_expires_at,
        )
        await self.__refresh_session_service.create_session(session_create_data)
        return AuthTokenData(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def create_tokens(self, auth_data: AuthData) -> Optional[AuthTokenData]:
        user = await self.__user_service.get_user_by_email(auth_data.email)
        password = auth_data.password.get_secret_value()
        if user is None:
            return None

        if not Hasher.verify_password(password, user.password_hash):
            return None

        return await self.__generate_tokens(user.id)

    async def logout(self, refresh_token: str) -> bool:
        token_data = await self.__get_user_token_data(refresh_token)
        if token_data is None:
            return False

        user, refresh_token_id = token_data
        refresh_service = self.__refresh_session_service
        user_active_session = await refresh_service.get_active_user_session(user.id)
        if user_active_session is None:
            return False

        if user_active_session.refresh_token_id != refresh_token_id:
            return False

        user_active_session.is_invalidated = True
        await self.__refresh_session_service.save_session(user_active_session)
        return True

    async def refresh_tokens(self, refresh_token: str) -> Optional[AuthTokenData]:
        token_data = await self.__get_user_token_data(refresh_token)
        if token_data is None:
            return None

        user, refresh_token_id = token_data
        refresh_service = self.__refresh_session_service
        user_active_session = await refresh_service.get_active_user_session(user.id)
        if user_active_session is None:
            return None

        if user_active_session.refresh_token_id != refresh_token_id:
            return None

        user_active_session.is_invalidated = True
        await self.__refresh_session_service.save_session(user_active_session)
        return await self.__generate_tokens(user.id)
