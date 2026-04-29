from typing import Optional

from sqlmodel import select

from app.models.entities.user import User
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    def __init__(self, session):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self._session.exec(stmt)
        return result.first()
