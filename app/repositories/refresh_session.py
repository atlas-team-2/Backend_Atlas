from typing import Optional, Sequence
from uuid import UUID

from sqlmodel import select

from app.models.entities.refresh_session import RefreshSession
from app.repositories.base import Repository


class RefreshSessionRepository(Repository[RefreshSession]):
    def __init__(self, session):
        super().__init__(session, RefreshSession)

    async def get_user_sessions(self, user_id: UUID) -> Sequence[RefreshSession]:
        stmt = select(RefreshSession).where(RefreshSession.user_id == user_id)
        result = await self._session.exec(stmt)
        return result.all()

    async def get_by_refresh_token_id(
        self,
        refresh_token_id: UUID,
    ) -> Optional[RefreshSession]:
        stmt = select(RefreshSession).where(
            RefreshSession.refresh_token_id == refresh_token_id,
        )
        result = await self._session.exec(stmt)
        return result.first()
