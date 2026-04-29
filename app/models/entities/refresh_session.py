from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Field, SQLModel

from app.models.base import BaseModel


class RefreshSessionBase(SQLModel):
    user_id: UUID = Field(foreign_key='user.id', index=True)
    access_token_id: UUID
    refresh_token_id: UUID = Field(index=True)
    expires_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
        nullable=False,
    )
    is_invalidated: bool = False


class RefreshSession(BaseModel, RefreshSessionBase, table=True):
    @property
    def is_valid(self) -> bool:
        return not self.is_invalidated and self.expires_at > datetime.now(timezone.utc)


class RefreshSessionCreate(RefreshSessionBase):
    pass


class RefreshSessionUpdate(SQLModel):
    is_invalidated: Optional[bool] = None
    access_token_id: Optional[UUID] = None
    refresh_token_id: Optional[UUID] = None
    expires_at: Optional[datetime] = None
