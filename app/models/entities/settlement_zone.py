from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import BaseModel


class SettlementZoneBase(SQLModel):
    nation_id: UUID = Field(foreign_key="nation.id")
    region_name: str
    polygon_data: list = Field(sa_column=Column(JSONB))
    color: Optional[str] = None


class SettlementZone(BaseModel, SettlementZoneBase, table=True):
    nation: "Nation" = Relationship(back_populates="zones")


class SettlementZoneCreate(SettlementZoneBase):
    pass


class SettlementZoneUpdate(SQLModel):
    nation_id: Optional[UUID] = None
    region_name: Optional[str] = None
    polygon_data: Optional[list] = None
    color: Optional[str] = None


class SettlementZonePublic(SettlementZoneBase, BaseModel):
    pass
