from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class GameQuestionBase(SQLModel):
    game_id: UUID = Field(foreign_key="game.id")
    question_text: str
    image_url: Optional[str] = None
    order_index: int


class GameQuestion(BaseModel, GameQuestionBase, table=True):
    game: "Game" = Relationship(back_populates="questions")
    options: list["GameOption"] = Relationship(back_populates="question")


class GameQuestionCreate(GameQuestionBase):
    pass


class GameQuestionUpdate(SQLModel):
    game_id: Optional[UUID] = None
    question_text: Optional[str] = None
    image_url: Optional[str] = None
    order_index: Optional[int] = None


class GameQuestionPublic(GameQuestionBase, BaseModel):
    pass
