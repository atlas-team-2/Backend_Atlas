from pydantic import BaseModel
from typing import Optional


class SettlementZoneBase(BaseModel):
    region_name: str
    polygon_data: list
    color: Optional[str] = None
    nation_id: str


class SettlementZoneCreate(SettlementZoneBase):
    pass


class SettlementZoneUpdate(BaseModel):
    region_name: Optional[str] = None
    polygon_data: Optional[list] = None
    color: Optional[str] = None
    nation_id: Optional[str] = None


class SettlementZonePublic(SettlementZoneBase):
    id: str
