from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import CostumeServiceDep
from app.models.entities.costume import CostumeCreate, CostumeUpdate, CostumePublic
from fastapi import Depends
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix="/costumes",
    tags=["costumes"],
)

@router.get("/")
async def get_costumes(
    service: CostumeServiceDep,
    filters: CommonListFilters = Depends(),
) -> Sequence[CostumePublic]:
    return await service.get_costumes(offset=filters.offset, limit=filters.limit)

@router.post("/")
async def create_costume(
    costume_create: CostumeCreate,
    service: CostumeServiceDep,
) -> CostumePublic:
    return await service.create_costume(costume_create)

@router.get("/{costume_id}")
async def get_costume(
    costume_id: UUID,
    service: CostumeServiceDep,
) -> Optional[CostumePublic]:
    return await service.get_costume(costume_id)

@router.put("/{costume_id}")
async def update_costume(
    costume_id: UUID,
    costume_update: CostumeUpdate,
    service: CostumeServiceDep,
) -> Optional[CostumePublic]:
    return await service.update_costume(costume_id, costume_update)

@router.delete("/{costume_id}")
async def delete_costume(
    costume_id: UUID,
    service: CostumeServiceDep,
) -> Optional[CostumePublic]:
    return await service.delete_costume(costume_id)
