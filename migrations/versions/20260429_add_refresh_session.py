"""add refresh sessions

Revision ID: 20260429addauth
Revises: 75930a939c48
Create Date: 2026-04-29 10:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = '20260429addauth'
down_revision: Union[str, Sequence[str], None] = '75930a939c48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'refreshsession',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('access_token_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('refresh_token_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('expires_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('is_invalidated', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_refreshsession_refresh_token_id'),
        'refreshsession',
        ['refresh_token_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_refreshsession_user_id'),
        'refreshsession',
        ['user_id'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_refreshsession_user_id'), table_name='refreshsession')
    op.drop_index(
        op.f('ix_refreshsession_refresh_token_id'),
        table_name='refreshsession',
    )
    op.drop_table('refreshsession')
