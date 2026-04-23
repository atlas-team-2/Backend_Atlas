from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import NationServiceDep
from app.models.entities.nation import NationCreate, NationUpdate, NationPublic
from fastapi import Depends
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix="/nations",
    tags=["nations"],
)

@router.get("/")
async def get_nations(
    service: NationServiceDep,
    filters: CommonListFilters = Depends(),
) -> Sequence[NationPublic]:
    return await service.get_nations(offset=filters.offset, limit=filters.limit)

@router.post("/")
async def create_nation(
    nation_create: NationCreate,
    service: NationServiceDep,
) -> NationPublic:
    return await service.create_nation(nation_create)

@router.get("/{nation_id}")
async def get_nation(
    nation_id: UUID,
    service: NationServiceDep,
) -> Optional[NationPublic]:
    return await service.get_nation(nation_id)

@router.put("/{nation_id}")
async def update_nation(
    nation_id: UUID,
    nation_update: NationUpdate,
    service: NationServiceDep,
) -> Optional[NationPublic]:
    return await service.update_nation(nation_id, nation_update)

@router.delete("/{nation_id}")
async def delete_nation(
    nation_id: UUID,
    service: NationServiceDep,
) -> Optional[NationPublic]:
    return await service.delete_nation(nation_id)
