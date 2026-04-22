from pydantic import BaseModel
from typing import Optional
from app.models.models import GameType


class GameBase(BaseModel):
    nation_id: str
    type: GameType
    title: str
    description: Optional[str] = None


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    nation_id: Optional[str] = None
    type: Optional[GameType] = None
    title: Optional[str] = None
    description: Optional[str] = None


class GamePublic(GameBase):
    id: str
