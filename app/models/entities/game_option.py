from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class GameOptionBase(SQLModel):
    question_id: UUID = Field(foreign_key="gamequestion.id")
    text: str
    is_correct: bool
    image_url: Optional[str] = None
    explanation: Optional[str] = None


class GameOption(BaseModel, GameOptionBase, table=True):
    question: "GameQuestion" = Relationship(back_populates="options")


class GameOptionCreate(GameOptionBase):
    pass


class GameOptionUpdate(SQLModel):
    question_id: Optional[UUID] = None
    text: Optional[str] = None
    is_correct: Optional[bool] = None
    image_url: Optional[str] = None
    explanation: Optional[str] = None
    test_field: str | None = None # УДАЛИТЬ ПОТОМ


class GameOptionPublic(GameOptionBase, BaseModel):
    pass
