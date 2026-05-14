from typing import Optional
from uuid import UUID

from app.dependencies.repositories import RefreshSessionRepositoryDep
from app.models.entities.refresh_session import RefreshSession, RefreshSessionCreate


class RefreshSessionService:
    def __init__(self, refresh_session_repository: RefreshSessionRepositoryDep):
        self.__refresh_session_repository = refresh_session_repository

    async def get_active_user_session(
        self,
        user_id: UUID,
    ) -> Optional[RefreshSession]:
        repository = self.__refresh_session_repository
        user_sessions = await repository.get_user_sessions(user_id)

        valid_sessions = [session for session in user_sessions if session.is_valid]

        if len(valid_sessions) != 1:
            return None

        return valid_sessions[0]

    async def has_user_active_session(self, user_id: UUID) -> bool:
        user_active_session = await self.get_active_user_session(user_id)
        return user_active_session is not None

    async def get_by_refresh_token_id(
        self,
        refresh_token_id: UUID,
    ) -> Optional[RefreshSession]:
        session = await self.__refresh_session_repository.get_by_refresh_token_id(
            refresh_token_id,
        )

        if session is None or not session.is_valid:
            return None

        return session

    async def save_session(self, session: RefreshSession) -> RefreshSession:
        return await self.__refresh_session_repository.save(session)

    async def create_session(
        self,
        session_create_data: RefreshSessionCreate,
    ) -> RefreshSession:
        instance = RefreshSession(
            **session_create_data.model_dump(),
        )

        return await self.__refresh_session_repository.save(instance)
