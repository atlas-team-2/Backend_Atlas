from typing import Annotated, Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies.services import SettlementZoneServiceDep
from app.models.entities.settlement_zone import SettlementZoneCreate, SettlementZoneUpdate, SettlementZonePublic
from fastapi import Depends
from app.schemas.filters import CommonListFilters

router = APIRouter(
    prefix="/settlement-zones",
    tags=["settlement-zones"],
)

@router.get("/")
async def get_settlement_zones(
    service: SettlementZoneServiceDep,
    filters: CommonListFilters = Depends(),
) -> Sequence[SettlementZonePublic]:
    return await service.get_settlement_zones(offset=filters.offset, limit=filters.limit)

@router.post("/")
async def create_settlement_zone(
    settlement_zone_create: SettlementZoneCreate,
    service: SettlementZoneServiceDep,
) -> SettlementZonePublic:
    return await service.create_settlement_zone(settlement_zone_create)

@router.get("/{zone_id}")
async def get_settlement_zone(
    zone_id: UUID,
    service: SettlementZoneServiceDep,
) -> Optional[SettlementZonePublic]:
    return await service.get_settlement_zone(zone_id)

@router.put("/{zone_id}")
async def update_settlement_zone(
    zone_id: UUID,
    settlement_zone_update: SettlementZoneUpdate,
    service: SettlementZoneServiceDep,
) -> Optional[SettlementZonePublic]:
    return await service.update_settlement_zone(zone_id, settlement_zone_update)

@router.delete("/{zone_id}")
async def delete_settlement_zone(
    zone_id: UUID,
    service: SettlementZoneServiceDep,
) -> Optional[SettlementZonePublic]:
    return await service.delete_settlement_zone(zone_id)
