from pydantic import BaseModel
from typing import Optional


class GameOptionBase(BaseModel):
    question_id: str
    text: str
    is_correct: bool
    image_url: Optional[str] = None
    explanation: Optional[str] = None


class GameOptionCreate(GameOptionBase):
    pass


class GameOptionUpdate(BaseModel):
    question_id: Optional[str] = None
    text: Optional[str] = None
    is_correct: Optional[bool] = None
    image_url: Optional[str] = None
    explanation: Optional[str] = None


class GameOptionPublic(GameOptionBase):
    id: str
