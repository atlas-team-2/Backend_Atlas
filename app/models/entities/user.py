# ruff: noqa: F821
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Relationship, SQLModel

from app.models.base import BaseModel

from .link_models import UserRole


class UserBase(SQLModel):
    email: EmailStr


class User(BaseModel, UserBase, table=True):
    password_hash: str
    roles: list['Role'] = Relationship(back_populates='users', link_model=UserRole)
    comments: list['Comment'] = Relationship(back_populates='user')


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserPublic(UserBase, BaseModel):
    pass
