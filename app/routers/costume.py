from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import CostumeServiceDep
from app.models.entities.costume import CostumeCreate, CostumePublic, CostumeUpdate
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/costumes',
    tags=['costumes'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['costume:read'])], responses=auth_responses)
async def get_costumes(
    service: CostumeServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[CostumePublic]:
    return await service.get_costumes(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['costume:create'])], responses=auth_responses)
async def create_costume(
    costume_create: CostumeCreate,
    service: CostumeServiceDep,
) -> CostumePublic:
    return await service.create_costume(costume_create)


@router.get('/{costume_id}', dependencies=[require_scopes(['costume:read'])], responses={**auth_responses, **detail_responses})
async def get_costume(
    costume_id: UUID,
    service: CostumeServiceDep,
) -> CostumePublic:
    result = await service.get_costume(costume_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{costume_id}', dependencies=[require_scopes(['costume:update'])], responses={**auth_responses, **detail_responses})
async def update_costume(
    costume_id: UUID,
    costume_update: CostumeUpdate,
    service: CostumeServiceDep,
) -> CostumePublic:
    result = await service.update_costume(costume_id, costume_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{costume_id}', dependencies=[require_scopes(['costume:delete'])], responses={**auth_responses, **detail_responses})
async def delete_costume(
    costume_id: UUID,
    service: CostumeServiceDep,
) -> CostumePublic:
    result = await service.delete_costume(costume_id)
    if result is None:
        raise NotFoundError()
    return result