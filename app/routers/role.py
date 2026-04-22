from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import RoleServiceDep
from app.models.entities.role import RoleCreate, RoleUpdate, RolePublic

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)

@router.get("/")
async def get_roles(
    service: RoleServiceDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
) -> Sequence[RolePublic]:
    return await service.get_roles(offset=offset, limit=limit)

@router.post("/")
async def create_role(
    role_create: RoleCreate,
    service: RoleServiceDep,
) -> RolePublic:
    return await service.create_role(role_create)

@router.get("/{role_id}")
async def get_role(
    role_id: UUID,
    service: RoleServiceDep,
) -> Optional[RolePublic]:
    return await service.get_role(role_id)

@router.put("/{role_id}")
async def update_role(
    role_id: UUID,
    role_update: RoleUpdate,
    service: RoleServiceDep,
) -> Optional[RolePublic]:
    return await service.update_role(role_id, role_update)

@router.delete("/{role_id}")
async def delete_role(
    role_id: UUID,
    service: RoleServiceDep,
) -> Optional[RolePublic]:
    return await service.delete_role(role_id)
