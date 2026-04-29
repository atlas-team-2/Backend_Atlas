from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import UserRepositoryDep
from app.models.entities.user import User, UserCreate, UserUpdate
from app.utils.hasher import Hasher


class UserService:
    def __init__(self, user_repository: UserRepositoryDep):
        self.user_repository = user_repository

    async def get_users(self, offset: int = 0, limit: int = 100) -> Sequence[User]:
        return await self.user_repository.fetch(offset=offset, limit=limit)

    async def create_user(self, user_create: UserCreate) -> User:
        data = user_create.model_dump()

        password = data.pop('password')
        password_hash = Hasher.get_password_hash(password)

        user = User(**data, password_hash=password_hash)
        return await self.user_repository.save(user)

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

        if 'password' in data and data['password'] is not None:
            password = data.pop('password')
            data['password_hash'] = Hasher.get_password_hash(password)

        return await self.user_repository.update(user_id, data)

    async def delete_user(self, user_id: UUID) -> Optional[User]:
        return await self.user_repository.delete(user_id)
