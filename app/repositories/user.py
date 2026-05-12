from typing import Optional
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.dependencies.session import SessionDep
from app.models.entities.role import Role
from app.models.entities.user import User
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    def __init__(self, session: SessionDep):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.fetch_one(
            filters={'email': email},
        )

    async def get_with_roles_permissions(self, user_id: UUID) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.roles).selectinload(Role.permissions))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
