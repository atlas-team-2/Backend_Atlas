from typing import Optional

from app.dependencies.session import SessionDep
from app.models.entities.user import User
from app.repositories.base import Repository


class UserRepository(Repository[User]):
    def __init__(self, session: SessionDep):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.fetch_one(
            filters={'email': email},
        )
