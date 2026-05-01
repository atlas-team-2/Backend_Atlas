from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

import jwt

from app.core.settings import settings
from app.dependencies.services import RefreshSessionServiceDep, UserServiceDep
from app.models.entities.refresh_session import RefreshSessionCreate
from app.models.entities.user import User, UserCreate
from app.schemas.auth import AuthData, AuthTokenData
from app.utils.hasher import Hasher


class Authenticator:
    def __init__(
        self,
        user_service: UserServiceDep,
        refresh_session_service: RefreshSessionServiceDep,
    ):
        self.__user_service = user_service
        self.__refresh_session_service = refresh_session_service


    def __create_token(
        self,
        user_id: UUID,
        token_id: UUID,
        expires_at: datetime,
        token_type: str,
    ) -> str:
        payload = {
            'sub': str(user_id),
            'jti': str(token_id),
            'type': token_type,
            'iat': int(datetime.now(timezone.utc).timestamp()),
            'exp': int(expires_at.timestamp()),
        }

        return jwt.encode(
            payload,
            settings.auth.secret.get_secret_value(),
            algorithm=settings.auth.algorithm,
        )

    def __decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.auth.secret.get_secret_value(),
                algorithms=[settings.auth.algorithm],
            )
        except jwt.ExpiredSignatureError as err:
            raise ValueError('Token has expired') from err

        except jwt.InvalidTokenError as err:
            raise ValueError('Invalid token') from err

    async def __get_user_token_data(
        self,
        token: str,
        expected_type: str,
    ) -> Optional[tuple[User, UUID]]:
        try:
            payload = self.__decode_token(token)

            if payload.get('type') != expected_type:
                return None

            user_id = UUID(payload['sub'])
            token_id = UUID(payload['jti'])
        except (KeyError, ValueError, TypeError):
            return None

        user = await self.__user_service.get_user(user_id)
        if user is None:
            return None

        return user, token_id


    async def authenticate_user(self, access_token: str) -> Optional[User]:
        token_data = await self.__get_user_token_data(
            access_token,
            expected_type='access',
        )
        if token_data is None:
            return None

        user, access_token_id = token_data

        session = await self.__refresh_session_service.get_active_user_session(user.id)
        if session is None:
            return None

        if session.access_token_id != access_token_id:
            return None

        return user

    async def __generate_tokens(self, user_id: UUID) -> AuthTokenData:
        now = datetime.now(timezone.utc)

        access_token_id = uuid4()
        refresh_token_id = uuid4()

        access_token_expires = now + settings.auth.access_token_lifetime
        refresh_token_expires = now + settings.auth.refresh_token_lifetime

        access_token = self.__create_token(
            user_id=user_id,
            token_id=access_token_id,
            expires_at=access_token_expires,
            token_type='access',
        )

        refresh_token = self.__create_token(
            user_id=user_id,
            token_id=refresh_token_id,
            expires_at=refresh_token_expires,
            token_type='refresh',
        )

        await self.__refresh_session_service.create_session(
            RefreshSessionCreate(
                user_id=user_id,
                access_token_id=access_token_id,
                refresh_token_id=refresh_token_id,
                expires_at=refresh_token_expires,
            )
        )

        return AuthTokenData(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def create_tokens(self, auth_data: AuthData) -> Optional[AuthTokenData]:
        user = await self.__user_service.get_user_by_email(auth_data.email)
        if user is None:
            return None

        if not Hasher.verify_password(
            auth_data.password.get_secret_value(),
            user.password_hash,
        ):
            return None

        return await self.__generate_tokens(user.id)

    async def register(self, user_create: UserCreate) -> AuthTokenData:
        user = await self.__user_service.create_user(user_create)
        return await self.__generate_tokens(user.id)


    async def logout(self, refresh_token: str) -> bool:
        token_data = await self.__get_user_token_data(
            refresh_token,
            expected_type='refresh',
        )
        if token_data is None:
            return False

        user, refresh_token_id = token_data

        session = await self.__refresh_session_service.get_active_user_session(user.id)
        if session is None:
            return False

        if session.refresh_token_id != refresh_token_id:
            return False

        session.is_invalidated = True
        await self.__refresh_session_service.save_session(session)

        return True


    async def refresh_tokens(self, refresh_token: str) -> Optional[AuthTokenData]:
        token_data = await self.__get_user_token_data(
            refresh_token,
            expected_type='refresh',
        )
        if token_data is None:
            return None

        user, refresh_token_id = token_data

        session = await self.__refresh_session_service.get_active_user_session(user.id)
        if session is None:
            return None

        if session.refresh_token_id != refresh_token_id:
            return None

        session.is_invalidated = True
        await self.__refresh_session_service.save_session(session)

        return await self.__generate_tokens(user.id)
