from pydantic import BaseModel
from typing import Optional


class GameQuestionBase(BaseModel):
    game_id: str
    question_text: str
    image_url: Optional[str] = None
    order_index: int


class GameQuestionCreate(GameQuestionBase):
    pass


class GameQuestionUpdate(BaseModel):
    game_id: Optional[str] = None
    question_text: Optional[str] = None
    image_url: Optional[str] = None
    order_index: Optional[int] = None


class GameQuestionPublic(GameQuestionBase):
    id: str
