"""remove user_id from comment add author_name

Revision ID: 2dbd1b6ad5b3
Revises: 20260429addauth
Create Date: 2026-05-26 21:39:08.303145

"""
from typing import Sequence, Union
import sqlmodel

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2dbd1b6ad5b3'
down_revision: Union[str, Sequence[str], None] = '20260429addauth'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('comment', sa.Column('author_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_constraint(op.f('comment_user_id_fkey'), 'comment', type_='foreignkey')
    op.drop_column('comment', 'user_id')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('comment', sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key(op.f('comment_user_id_fkey'), 'comment', 'user', ['user_id'], ['id'])
    op.drop_column('comment', 'author_name')
