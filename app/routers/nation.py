from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import NationServiceDep
from app.models.entities.nation import NationCreate, NationPublic, NationUpdate
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/nations',
    tags=['nations'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['nation:read'])], responses=auth_responses)
async def get_nations(
    service: NationServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[NationPublic]:
    return await service.get_nations(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['nation:create'])], responses=auth_responses)
async def create_nation(
    nation_create: NationCreate,
    service: NationServiceDep,
) -> NationPublic:
    return await service.create_nation(nation_create)


@router.get('/{nation_id}', dependencies=[require_scopes(['nation:read'])], responses={**auth_responses, **detail_responses})
async def get_nation(
    nation_id: UUID,
    service: NationServiceDep,
) -> NationPublic:
    result = await service.get_nation(nation_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{nation_id}', dependencies=[require_scopes(['nation:update'])], responses={**auth_responses, **detail_responses})
async def update_nation(
    nation_id: UUID,
    nation_update: NationUpdate,
    service: NationServiceDep,
) -> NationPublic:
    result = await service.update_nation(nation_id, nation_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{nation_id}', dependencies=[require_scopes(['nation:delete'])], responses={**auth_responses, **detail_responses})
async def delete_nation(
    nation_id: UUID,
    service: NationServiceDep,
) -> NationPublic:
    result = await service.delete_nation(nation_id)
    if result is None:
        raise NotFoundError()
    return result