from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import UserRepositoryDep
from app.models.entities.user import User, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepositoryDep):
        self.user_repository = user_repository

    async def get_users(self, offset: int = 0, limit: int = 100) -> Sequence[User]:
        return await self.user_repository.fetch(offset=offset, limit=limit)

    async def create_user(self, user_data: dict) -> User:
        return await self.user_repository.save(User(**user_data))

    async def get_user(self, user_id: UUID) -> Optional[User]:
        return await self.user_repository.get(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.get_by_email(email)

    async def update_user(
        self,
        user_id: UUID,
        user_update: UserUpdate,
    ) -> Optional[User]:
        data = user_update.model_dump(exclude_unset=True)
        data.pop('password', None)

        return await self.user_repository.update(user_id, data)

    async def delete_user(self, user_id: UUID) -> Optional[User]:
        return await self.user_repository.delete(user_id)
