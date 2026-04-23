from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import RoleRepositoryDep
from app.models.entities.role import Role, RoleCreate, RoleUpdate, RolePublic

class RoleService:
    def __init__(self, role_repository: RoleRepositoryDep):
        self.role_repository = role_repository

    async def get_roles(self, offset: int = 0, limit: int = 100) -> Sequence[Role]:
        return await self.role_repository.fetch(offset=offset, limit=limit)

    async def create_role(self, role_create: RoleCreate) -> Role:
        role = Role(**role_create.model_dump())
        return await self.role_repository.save(role)

    async def get_role(self, role_id: UUID) -> Optional[Role]:
        return await self.role_repository.get(role_id)

    async def update_role(self, role_id: UUID, role_update: RoleUpdate) -> Optional[Role]:
        data = role_update.model_dump(exclude_unset=True)
        return await self.role_repository.update(role_id, data)

    async def delete_role(self, role_id: UUID) -> Optional[Role]:
        return await self.role_repository.delete(role_id)
