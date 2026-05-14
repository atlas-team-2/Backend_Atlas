from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.auth import require_scopes
from app.dependencies.services import PermissionServiceDep
from app.models.entities.permission import (
    PermissionCreate,
    PermissionPublic,
    PermissionUpdate,
)
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix='/permissions',
    tags=['permissions'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['permission:read'])])
async def get_permissions(
    service: PermissionServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[PermissionPublic]:
    return await service.get_permissions(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['permission:create'])])
async def create_permission(
    permission_create: PermissionCreate,
    service: PermissionServiceDep,
) -> PermissionPublic:
    return await service.create_permission(permission_create)


@router.get('/{permission_id}', dependencies=[require_scopes(['permission:read'])])
async def get_permission(
    permission_id: UUID,
    service: PermissionServiceDep,
) -> Optional[PermissionPublic]:
    return await service.get_permission(permission_id)


@router.put('/{permission_id}', dependencies=[require_scopes(['permission:update'])])
async def update_permission(
    permission_id: UUID,
    permission_update: PermissionUpdate,
    service: PermissionServiceDep,
) -> Optional[PermissionPublic]:
    return await service.update_permission(permission_id, permission_update)


@router.delete('/{permission_id}', dependencies=[require_scopes(['permission:delete'])])
async def delete_permission(
    permission_id: UUID,
    service: PermissionServiceDep,
) -> Optional[PermissionPublic]:
    return await service.delete_permission(permission_id)
