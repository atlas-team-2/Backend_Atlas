from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class NationBase(SQLModel):
    name: str = Field(index=True, unique=True)
    slug: str = Field(index=True, unique=True)
    population: Optional[int] = None
    image_url: Optional[str] = None


class Nation(BaseModel, NationBase, table=True):
    info: Optional["NationInfo"] = Relationship(back_populates="nation")
    zones: list["SettlementZone"] = Relationship(back_populates="nation")
    costumes: list["Costume"] = Relationship(back_populates="nation")
    comments: list["Comment"] = Relationship(back_populates="nation")
    games: list["Game"] = Relationship(back_populates="nation")


class NationCreate(NationBase):
    pass


class NationUpdate(SQLModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    population: Optional[int] = None
    image_url: Optional[str] = None


class NationPublic(NationBase, BaseModel):
    pass
