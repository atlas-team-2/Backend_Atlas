from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import RoleServiceDep
from app.models.entities.role import RoleCreate, RolePublic, RoleUpdate
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/roles',
    tags=['roles'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['role:read'])], responses=auth_responses)
async def get_roles(
    service: RoleServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[RolePublic]:
    return await service.get_roles(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['role:create'])], responses=auth_responses)
async def create_role(
    role_create: RoleCreate,
    service: RoleServiceDep,
) -> RolePublic:
    return await service.create_role(role_create)


@router.get('/{role_id}', dependencies=[require_scopes(['role:read'])], responses={**auth_responses, **detail_responses})
async def get_role(
    role_id: UUID,
    service: RoleServiceDep,
) -> RolePublic:
    result = await service.get_role(role_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{role_id}', dependencies=[require_scopes(['role:update'])], responses={**auth_responses, **detail_responses})
async def update_role(
    role_id: UUID,
    role_update: RoleUpdate,
    service: RoleServiceDep,
) -> RolePublic:
    result = await service.update_role(role_id, role_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{role_id}', dependencies=[require_scopes(['role:delete'])], responses={**auth_responses, **detail_responses})
async def delete_role(
    role_id: UUID,
    service: RoleServiceDep,
) -> RolePublic:
    result = await service.delete_role(role_id)
    if result is None:
        raise NotFoundError()
    return result