from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import PermissionRepositoryDep
from app.models.entities.permission import Permission, PermissionCreate, PermissionUpdate, PermissionPublic

class PermissionService:
    def __init__(self, permission_repository: PermissionRepositoryDep):
        self.permission_repository = permission_repository

    async def get_permissions(self, offset: int = 0, limit: int = 100) -> Sequence[Permission]:
        return await self.permission_repository.fetch(offset=offset, limit=limit)

    async def create_permission(self, permission_create: PermissionCreate) -> Permission:
        permission = Permission(**permission_create.model_dump())
        return await self.permission_repository.save(permission)

    async def get_permission(self, permission_id: UUID) -> Optional[Permission]:
        return await self.permission_repository.get(permission_id)

    async def update_permission(self, permission_id: UUID, permission_update: PermissionUpdate) -> Optional[Permission]:
        data = permission_update.model_dump(exclude_unset=True)
        return await self.permission_repository.update(permission_id, data)

    async def delete_permission(self, permission_id: UUID) -> Optional[Permission]:
        return await self.permission_repository.delete(permission_id)
