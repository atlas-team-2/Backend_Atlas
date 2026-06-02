from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.dependencies.session import SessionDep
from app.models.entities.role import Role
from app.repositories.base import Repository


class RoleRepository(Repository[Role]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Role)

    async def get_by_name(self, name: str) -> Optional[Role]:
        return await self.fetch_one(filters={'name': name})

    async def get_by_name_with_permissions(self, name: str) -> Optional[Role]:
        stmt = (
            select(Role)
            .where(Role.name == name)
            .options(selectinload(Role.permissions))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
