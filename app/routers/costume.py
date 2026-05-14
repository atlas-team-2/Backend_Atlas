from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.auth import require_scopes
from app.dependencies.services import CostumeServiceDep
from app.models.entities.costume import CostumeCreate, CostumePublic, CostumeUpdate
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix='/costumes',
    tags=['costumes'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['costume:read'])])
async def get_costumes(
    service: CostumeServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[CostumePublic]:
    return await service.get_costumes(offset=filters.offset, limit=filters.limit)


@router.post('/', dependencies=[require_scopes(['costume:create'])])
async def create_costume(
    costume_create: CostumeCreate,
    service: CostumeServiceDep,
) -> CostumePublic:
    return await service.create_costume(costume_create)


@router.get('/{costume_id}', dependencies=[require_scopes(['costume:read'])])
async def get_costume(
    costume_id: UUID,
    service: CostumeServiceDep,
) -> Optional[CostumePublic]:
    return await service.get_costume(costume_id)


@router.put('/{costume_id}', dependencies=[require_scopes(['costume:update'])])
async def update_costume(
    costume_id: UUID,
    costume_update: CostumeUpdate,
    service: CostumeServiceDep,
) -> Optional[CostumePublic]:
    return await service.update_costume(costume_id, costume_update)


@router.delete('/{costume_id}', dependencies=[require_scopes(['costume:delete'])])
async def delete_costume(
    costume_id: UUID,
    service: CostumeServiceDep,
) -> Optional[CostumePublic]:
    return await service.delete_costume(costume_id)
