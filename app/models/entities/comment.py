from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class CommentBase(SQLModel):
    nation_id: UUID = Field(foreign_key="nation.id")
    user_id: UUID = Field(foreign_key="user.id")
    text: str
    is_approved: bool


class Comment(BaseModel, CommentBase, table=True):
    nation: "Nation" = Relationship(back_populates="comments")
    user: "User" = Relationship(back_populates="comments")


class CommentCreate(SQLModel):
    nation_id: UUID
    user_id: UUID
    text: str


class CommentUpdate(SQLModel):
    text: Optional[str] = None
    is_approved: Optional[bool] = None


class CommentPublic(CommentBase, BaseModel):
    pass
