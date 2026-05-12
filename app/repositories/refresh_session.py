from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.session import SessionDep
from app.models.entities.refresh_session import RefreshSession
from app.repositories.base import Repository


class RefreshSessionRepository(Repository[RefreshSession]):
    def __init__(self, session: SessionDep):
        super().__init__(session, RefreshSession)

    async def get_user_sessions(self, user_id: UUID) -> Sequence[RefreshSession]:
        return await self.fetch(
            filters={'user_id': user_id},
        )

    async def get_by_refresh_token_id(
        self,
        refresh_token_id: UUID,
    ) -> Optional[RefreshSession]:
        return await self.fetch_one(
            filters={'refresh_token_id': refresh_token_id},
        )
