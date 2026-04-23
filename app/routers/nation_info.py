from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import NationInfoServiceDep
from app.models.entities.nation_info import NationInfoCreate, NationInfoUpdate, NationInfoPublic
from fastapi import Depends
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix="/nation-infos",
    tags=["nation-infos"],
)

@router.get("/")
async def get_nation_infos(
    service: NationInfoServiceDep,
    filters: CommonListFilters = Depends(),
) -> Sequence[NationInfoPublic]:
    return await service.get_nation_infos(offset=filters.offset, limit=filters.limit)

@router.post("/")
async def create_nation_info(
    nation_info_create: NationInfoCreate,
    service: NationInfoServiceDep,
) -> NationInfoPublic:
    return await service.create_nation_info(nation_info_create)

@router.get("/{info_id}")
async def get_nation_info(
    info_id: UUID,
    service: NationInfoServiceDep,
) -> Optional[NationInfoPublic]:
    return await service.get_nation_info(info_id)

@router.put("/{info_id}")
async def update_nation_info(
    info_id: UUID,
    nation_info_update: NationInfoUpdate,
    service: NationInfoServiceDep,
) -> Optional[NationInfoPublic]:
    return await service.update_nation_info(info_id, nation_info_update)

@router.delete("/{info_id}")
async def delete_nation_info(
    info_id: UUID,
    service: NationInfoServiceDep,
) -> Optional[NationInfoPublic]:
    return await service.delete_nation_info(info_id)
