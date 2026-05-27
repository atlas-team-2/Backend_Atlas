"""add email notification table

Revision ID: e596e1421753
Revises: 2dbd1b6ad5b3
Create Date: 2026-05-26 22:18:27.542281

"""
from typing import Sequence, Union
import sqlmodel

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e596e1421753'
down_revision: Union[str, Sequence[str], None] = '2dbd1b6ad5b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('emailnotification',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('action', sa.Enum('VERIFY_ACCOUNT', 'CHANGE_PASSWORD', name='emailaction'), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('is_used', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('emailnotification')
