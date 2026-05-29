from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel


class RolePermission(SQLModel, table=True):
    role_id: UUID = Field(
        sa_column=sa.Column(
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey('role.id'),
            primary_key=True,
        ),
    )
    permission_id: UUID = Field(
        sa_column=sa.Column(
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey('permission.id'),
            primary_key=True,
        ),
    )


class UserRole(SQLModel, table=True):
    user_id: UUID = Field(
        sa_column=sa.Column(
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey('user.id'),
            primary_key=True,
        ),
    )
    role_id: UUID = Field(
        sa_column=sa.Column(
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey('role.id'),
            primary_key=True,
        ),
    )
