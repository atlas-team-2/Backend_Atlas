from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.responses import auth_responses, detail_responses
from app.dependencies.auth import require_scopes
from app.dependencies.services import SettlementZoneServiceDep
from app.models.entities.settlement_zone import (
    SettlementZoneCreate,
    SettlementZonePublic,
    SettlementZoneUpdate,
)
from app.schemas.filters import CommonListFilters
from app.utils.errors import NotFoundError

router = APIRouter(
    prefix='/settlement-zones',
    tags=['settlement-zones'],
)

CommonListFiltersDep = Annotated[CommonListFilters, Depends()]


@router.get('/', dependencies=[require_scopes(['settlement_zone:read'])], responses=auth_responses)
async def get_settlement_zones(
    service: SettlementZoneServiceDep,
    filters: CommonListFiltersDep,
) -> Sequence[SettlementZonePublic]:
    return await service.get_settlement_zones(
        offset=filters.offset,
        limit=filters.limit,
    )


@router.post('/', dependencies=[require_scopes(['settlement_zone:create'])], responses=auth_responses)
async def create_settlement_zone(
    settlement_zone_create: SettlementZoneCreate,
    service: SettlementZoneServiceDep,
) -> SettlementZonePublic:
    return await service.create_settlement_zone(settlement_zone_create)


@router.get('/{zone_id}', dependencies=[require_scopes(['settlement_zone:read'])], responses={**auth_responses, **detail_responses})
async def get_settlement_zone(
    zone_id: UUID,
    service: SettlementZoneServiceDep,
) -> SettlementZonePublic:
    result = await service.get_settlement_zone(zone_id)
    if result is None:
        raise NotFoundError()
    return result


@router.put('/{zone_id}', dependencies=[require_scopes(['settlement_zone:update'])], responses={**auth_responses, **detail_responses})
async def update_settlement_zone(
    zone_id: UUID,
    settlement_zone_update: SettlementZoneUpdate,
    service: SettlementZoneServiceDep,
) -> SettlementZonePublic:
    result = await service.update_settlement_zone(zone_id, settlement_zone_update)
    if result is None:
        raise NotFoundError()
    return result


@router.delete('/{zone_id}', dependencies=[require_scopes(['settlement_zone:delete'])], responses={**auth_responses, **detail_responses})
async def delete_settlement_zone(
    zone_id: UUID,
    service: SettlementZoneServiceDep,
) -> SettlementZonePublic:
    result = await service.delete_settlement_zone(zone_id)
    if result is None:
        raise NotFoundError()
    return result