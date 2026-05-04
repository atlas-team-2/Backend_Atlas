from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import computed_field
from sqlalchemy import TIMESTAMP, Column
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RefreshSessionCreate(SQLModel):
    user_id: UUID = Field(foreign_key='user.id')
    access_token_id: UUID
    refresh_token_id: UUID
    expires_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
        ),
    )


class RefreshSession(RefreshSessionCreate, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )
    is_invalidated: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
        ),
    )

    @computed_field
    @property
    def is_valid(self) -> bool:
        now = datetime.now(timezone.utc)
        expired = now > self.expires_at
        is_invalid = expired or self.is_invalidated

        return not is_invalid
