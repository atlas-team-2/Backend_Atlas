from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class CostumeBase(SQLModel):
    nation_id: UUID = Field(foreign_key="nation.id")
    gender: Gender
    image_url: str
    description: Optional[str] = None


class Costume(BaseModel, CostumeBase, table=True):
    nation: "Nation" = Relationship(back_populates="costumes")


class CostumeCreate(CostumeBase):
    pass


class CostumeUpdate(SQLModel):
    nation_id: Optional[UUID] = None
    gender: Optional[Gender] = None
    image_url: Optional[str] = None
    description: Optional[str] = None


class CostumePublic(CostumeBase, BaseModel):
    pass
