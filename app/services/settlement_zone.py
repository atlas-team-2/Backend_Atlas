from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import SettlementZoneRepositoryDep
from app.models.entities.settlement_zone import SettlementZone, SettlementZoneCreate, SettlementZoneUpdate, SettlementZonePublic

class SettlementZoneService:
    def __init__(self, settlement_zone_repository: SettlementZoneRepositoryDep):
        self.settlement_zone_repository = settlement_zone_repository

    async def get_settlement_zones(self, offset: int = 0, limit: int = 100) -> Sequence[SettlementZone]:
        return await self.settlement_zone_repository.fetch(offset=offset, limit=limit)

    async def create_settlement_zone(self, settlement_zone_create: SettlementZoneCreate) -> SettlementZone:
        zone = SettlementZone(**settlement_zone_create.model_dump())
        return await self.settlement_zone_repository.save(zone)

    async def get_settlement_zone(self, zone_id: UUID) -> Optional[SettlementZone]:
        return await self.settlement_zone_repository.get(zone_id)

    async def update_settlement_zone(self, zone_id: UUID, settlement_zone_update: SettlementZoneUpdate) -> Optional[SettlementZone]:
        data = settlement_zone_update.model_dump(exclude_unset=True)
        return await self.settlement_zone_repository.update(zone_id, data)

    async def delete_settlement_zone(self, zone_id: UUID) -> Optional[SettlementZone]:
        return await self.settlement_zone_repository.delete(zone_id)
