from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.auth import require_scopes
from app.dependencies.services import NationServiceDep
from app.models.entities.nation import NationCreate, NationPublic, NationUpdate
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix='/nations',
    tags=['nations'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['nation:read'])])
async def get_nations(
    service: NationServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[NationPublic]:
    return await service.get_nations(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['nation:create'])])
async def create_nation(
    nation_create: NationCreate,
    service: NationServiceDep,
) -> NationPublic:
    return await service.create_nation(nation_create)


@router.get('/{nation_id}', dependencies=[require_scopes(['nation:read'])])
async def get_nation(
    nation_id: UUID,
    service: NationServiceDep,
) -> Optional[NationPublic]:
    return await service.get_nation(nation_id)


@router.put('/{nation_id}', dependencies=[require_scopes(['nation:update'])])
async def update_nation(
    nation_id: UUID,
    nation_update: NationUpdate,
    service: NationServiceDep,
) -> Optional[NationPublic]:
    return await service.update_nation(nation_id, nation_update)


@router.delete('/{nation_id}', dependencies=[require_scopes(['nation:delete'])])
async def delete_nation(
    nation_id: UUID,
    service: NationServiceDep,
) -> Optional[NationPublic]:
    return await service.delete_nation(nation_id)
