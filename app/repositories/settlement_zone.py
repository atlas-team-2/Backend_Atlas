from app.models.entities.settlement_zone import SettlementZone
from app.repositories.base import Repository

class SettlementZoneRepository(Repository[SettlementZone]):
    def __init__(self, session):
        super().__init__(session, SettlementZone)
