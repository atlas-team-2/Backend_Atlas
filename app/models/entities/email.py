# ruff: noqa: F821
from enum import IntEnum
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.base import BaseModel


class EmailAction(IntEnum):
    VERIFY_ACCOUNT = 0
    CHANGE_PASSWORD = 1


class EmailNotificationBase(SQLModel):
    user_id: UUID = Field(foreign_key='user.id')
    code: str
    action: EmailAction


class EmailNotification(BaseModel, EmailNotificationBase, table=True):
    is_used: bool = False


class EmailNotificationCreate(EmailNotificationBase):
    pass