from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import PermissionServiceDep
from app.models.entities.permission import (
    PermissionCreate,
    PermissionPublic,
    PermissionUpdate,
)
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/permissions',
    tags=['permissions'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['permission:read'])], responses=auth_responses)
async def get_permissions(
    service: PermissionServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[PermissionPublic]:
    return await service.get_permissions(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['permission:create'])], responses=auth_responses)
async def create_permission(
    permission_create: PermissionCreate,
    service: PermissionServiceDep,
) -> PermissionPublic:
    return await service.create_permission(permission_create)


@router.get('/{permission_id}', dependencies=[require_scopes(['permission:read'])], responses={**auth_responses, **detail_responses})
async def get_permission(
    permission_id: UUID,
    service: PermissionServiceDep,
) -> PermissionPublic:
    result = await service.get_permission(permission_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{permission_id}', dependencies=[require_scopes(['permission:update'])], responses={**auth_responses, **detail_responses})
async def update_permission(
    permission_id: UUID,
    permission_update: PermissionUpdate,
    service: PermissionServiceDep,
) -> PermissionPublic:
    result = await service.update_permission(permission_id, permission_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{permission_id}', dependencies=[require_scopes(['permission:delete'])], responses={**auth_responses, **detail_responses})
async def delete_permission(
    permission_id: UUID,
    service: PermissionServiceDep,
) -> PermissionPublic:
    result = await service.delete_permission(permission_id)
    if result is None:
        raise NotFoundError()
    return result