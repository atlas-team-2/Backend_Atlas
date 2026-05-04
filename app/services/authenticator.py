from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

import jwt

from app.core.settings import settings
from app.dependencies.services import RefreshSessionServiceDep, UserServiceDep
from app.models.entities.refresh_session import RefreshSession, RefreshSessionCreate
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

    def __create_user_token(
        self,
        user_id: UUID,
        token_id: UUID,
        expires_at: datetime,
    ) -> str:
        payload = {
            'sub': str(user_id),
            'exp': expires_at,
            'jti': str(token_id),
            'iat': datetime.now(timezone.utc),
        }

        return jwt.encode(
            payload=payload,
            key=settings.auth.secret.get_secret_value(),
            algorithm=settings.auth.algorithm,
        )

    def __decode_token(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(
                jwt=token,
                key=settings.auth.secret.get_secret_value(),
                algorithms=[settings.auth.algorithm],
            )
        except jwt.PyJWTError:
            return None

    async def __get_user_token_data(
        self,
        token: str,
    ) -> Optional[tuple[RefreshSession, UUID, UUID]]:
        decoded_payload = self.__decode_token(token)

        if decoded_payload is None:
            return None

        try:
            raw_user_id = decoded_payload.get('sub')
            raw_token_id = decoded_payload.get('jti')

            user_id = UUID(raw_user_id)
            token_id = UUID(raw_token_id)
        except (TypeError, ValueError):
            return None

        user_active_session = (
            await self.__refresh_session_service.get_active_user_session(
                user_id,
            )
        )

        if user_active_session is None:
            return None

        return user_active_session, user_id, token_id

    async def register(self, user_create: UserCreate) -> bool:
        data = user_create.model_dump()

        password = data.pop('password')

        if hasattr(password, 'get_secret_value'):
            password = password.get_secret_value()

        data['password_hash'] = Hasher.get_password_hash(password)

        await self.__user_service.create_user(data)
        return True

    async def authenticate_user(self, access_token: str) -> Optional[User]:
        token_data = await self.__get_user_token_data(access_token)

        if token_data is None:
            return None

        user_active_session, user_id, access_token_id = token_data

        if user_active_session.access_token_id != access_token_id:
            return None

        return await self.__user_service.get_user(user_id)

    async def create_tokens(self, auth_data: AuthData) -> Optional[AuthTokenData]:
        user = await self.__user_service.get_user_by_email(auth_data.email)

        if user is None:
            return None

        password = auth_data.password.get_secret_value()

        if not Hasher.verify_password(password, user.password_hash):
            return None

        return await self.__generate_tokens(user.id)

    async def refresh_tokens(self, refresh_token: str) -> Optional[AuthTokenData]:
        token_data = await self.__get_user_token_data(refresh_token)

        if token_data is None:
            return None

        user_active_session, user_id, refresh_token_id = token_data

        if user_active_session.refresh_token_id != refresh_token_id:
            return None

        user_active_session.is_invalidated = True
        await self.__refresh_session_service.save_session(user_active_session)

        return await self.__generate_tokens(user_id)

    async def logout(self, refresh_token: str) -> bool:
        token_data = await self.__get_user_token_data(refresh_token)

        if token_data is None:
            return False

        user_active_session, _, refresh_token_id = token_data

        if user_active_session.refresh_token_id != refresh_token_id:
            return False

        user_active_session.is_invalidated = True
        await self.__refresh_session_service.save_session(user_active_session)

        return True

    async def __generate_tokens(self, user_id: UUID) -> Optional[AuthTokenData]:
        has_active_session = (
            await self.__refresh_session_service.has_user_active_session(
                user_id,
            )
        )

        if has_active_session:
            return None

        now = datetime.now(timezone.utc)

        access_token_id = uuid4()
        access_token_expires_at = now + settings.auth.access_token_lifetime

        access_token = self.__create_user_token(
            user_id=user_id,
            token_id=access_token_id,
            expires_at=access_token_expires_at,
        )

        refresh_token_id = uuid4()
        refresh_token_expires_at = now + settings.auth.refresh_token_lifetime

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
