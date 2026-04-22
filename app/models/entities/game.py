from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel
from enum import Enum


class GameType(str, Enum):
    dish = "dish"
    holiday = "holiday"
    ornament = "ornament"


class GameBase(SQLModel):
    nation_id: UUID = Field(foreign_key="nation.id")
    type: GameType
    title: str
    description: Optional[str] = None


class Game(BaseModel, GameBase, table=True):
    nation: "Nation" = Relationship(back_populates="games")
    questions: list["GameQuestion"] = Relationship(back_populates="game")


class GameCreate(GameBase):
    pass


class GameUpdate(SQLModel):
    nation_id: Optional[UUID] = None
    type: Optional[GameType] = None
    title: Optional[str] = None
    description: Optional[str] = None


class GamePublic(GameBase, BaseModel):
    pass
