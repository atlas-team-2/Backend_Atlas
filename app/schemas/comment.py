from pydantic import BaseModel
from typing import Optional


class CommentBase(BaseModel):
    nation_id: str
    user_id: str
    text: str
    is_approved: bool


class CommentCreate(BaseModel):
    nation_id: str
    user_id: str
    text: str


class CommentUpdate(BaseModel):
    text: Optional[str] = None
    is_approved: Optional[bool] = None


class CommentPublic(CommentBase):
    id: str
