from typing import Optional

from app.dependencies.session import SessionDep
from app.models.entities.permission import Permission
from app.repositories.base import Repository


class PermissionRepository(Repository[Permission]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Permission)

    async def get_by_scope(self, subject: str, action: str) -> Optional[Permission]:
        return await self.fetch_one(filters={'subject': subject, 'action': action})
