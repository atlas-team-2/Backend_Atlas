from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import PermissionServiceDep
from app.models.entities.permission import PermissionCreate, PermissionUpdate, PermissionPublic

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
)

@router.get("/")
async def get_permissions(
    service: PermissionServiceDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
) -> Sequence[PermissionPublic]:
    return await service.get_permissions(offset=offset, limit=limit)

@router.post("/")
async def create_permission(
    permission_create: PermissionCreate,
    service: PermissionServiceDep,
) -> PermissionPublic:
    return await service.create_permission(permission_create)

@router.get("/{permission_id}")
async def get_permission(
    permission_id: UUID,
    service: PermissionServiceDep,
) -> Optional[PermissionPublic]:
    return await service.get_permission(permission_id)

@router.put("/{permission_id}")
async def update_permission(
    permission_id: UUID,
    permission_update: PermissionUpdate,
    service: PermissionServiceDep,
) -> Optional[PermissionPublic]:
    return await service.update_permission(permission_id, permission_update)

@router.delete("/{permission_id}")
async def delete_permission(
    permission_id: UUID,
    service: PermissionServiceDep,
) -> Optional[PermissionPublic]:
    return await service.delete_permission(permission_id)
