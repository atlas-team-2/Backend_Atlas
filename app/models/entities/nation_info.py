from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import BaseModel


class NationInfoBase(SQLModel):
    nation_id: UUID = Field(foreign_key="nation.id")
    origin: str
    self_name: str
    language: list[str] = Field(sa_column=Column(JSONB))
    religion: list[str] = Field(sa_column=Column(JSONB))
    facts: Optional[list[str]] = Field(default=None, sa_column=Column(JSONB))


class NationInfo(BaseModel, NationInfoBase, table=True):
    nation: "Nation" = Relationship(back_populates="info")


class NationInfoCreate(NationInfoBase):
    pass


class NationInfoUpdate(SQLModel):
    nation_id: Optional[UUID] = None
    origin: Optional[str] = None
    self_name: Optional[str] = None
    language: Optional[list[str]] = None
    religion: Optional[list[str]] = None
    facts: Optional[list[str]] = None


class NationInfoPublic(NationInfoBase, BaseModel):
    pass
