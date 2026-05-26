from typing import Optional, Sequence
from uuid import UUID

from app.core.settings import settings
from app.dependencies.repositories import RoleRepositoryDep, UserRepositoryDep
from app.models.entities.user import User, UserUpdate


class UserService:
    def __init__(
        self,
        user_repository: UserRepositoryDep,
        role_repository: RoleRepositoryDep,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def get_users(self, offset: int = 0, limit: int = 100) -> Sequence[User]:
        return await self.user_repository.fetch(offset=offset, limit=limit)

    async def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        public_role = await self.role_repository.get_by_name(settings.rbac.public_role)
        if public_role is not None:
            user.roles = [public_role]
        return await self.user_repository.save(user)

    async def get_user(self, user_id: UUID) -> Optional[User]:
        return await self.user_repository.get(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.get_by_email(email)

    async def get_user_scopes(self, user_id: UUID) -> list[str]:
        user = await self.user_repository.get_with_roles_permissions(user_id)

        if user is None:
            return []

        scopes = {
            f'{permission.subject}:{permission.action}'
            for role in user.roles
            for permission in role.permissions
        }

        return sorted(scopes)

    async def assign_role(self, user_id: UUID, role_id: UUID) -> Optional[User]:
        user = await self.user_repository.get_with_roles_permissions(user_id)
        if user is None:
            return None
        role = await self.role_repository.get(role_id)
        if role is None:
            return None
        if role.id not in {r.id for r in user.roles}:
            user.roles.append(role)
            await self.user_repository.save(user)
        return user

    async def revoke_role(self, user_id: UUID, role_id: UUID) -> Optional[User]:
        user = await self.user_repository.get_with_roles_permissions(user_id)
        if user is None:
            return None
        user.roles = [r for r in user.roles if r.id != role_id]
        await self.user_repository.save(user)
        return user

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

    async def update_password_hash(self, user_id: UUID, password_hash: str) -> Optional[User]:
        return await self.user_repository.update(user_id, {'password_hash': password_hash})
