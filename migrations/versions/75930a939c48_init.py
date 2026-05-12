"""init

Revision ID: 75930a939c48
Revises:
Create Date: 2026-04-23 21:41:12.963251

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = '75930a939c48'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    uuid_type = postgresql.UUID(as_uuid=True)

    gender_enum = postgresql.ENUM(
        'MALE',
        'FEMALE',
        name='gender',
        create_type=False,
    )
    game_type_enum = postgresql.ENUM(
        'DISH',
        'HOLIDAY',
        'ORNAMENT',
        name='gametype',
        create_type=False,
    )

    gender_enum.create(op.get_bind(), checkfirst=True)
    game_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'nation',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('population', sa.Integer(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_nation_name'), 'nation', ['name'], unique=True)
    op.create_index(op.f('ix_nation_slug'), 'nation', ['slug'], unique=True)

    op.create_table(
        'permission',
        sa.Column('subject', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'role',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    op.create_table(
        'user',
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'comment',
        sa.Column('nation_id', uuid_type, nullable=False),
        sa.Column('user_id', uuid_type, nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('is_approved', sa.Boolean(), nullable=False),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['nation_id'], ['nation.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'costume',
        sa.Column('nation_id', uuid_type, nullable=False),
        sa.Column('gender', gender_enum, nullable=False),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['nation_id'], ['nation.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'game',
        sa.Column('nation_id', uuid_type, nullable=False),
        sa.Column('type', game_type_enum, nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['nation_id'], ['nation.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'nationinfo',
        sa.Column('nation_id', uuid_type, nullable=False),
        sa.Column('origin', sa.String(), nullable=False),
        sa.Column('self_name', sa.String(), nullable=False),
        sa.Column('language', postgresql.JSONB(), nullable=False),
        sa.Column('religion', postgresql.JSONB(), nullable=False),
        sa.Column('facts', postgresql.JSONB(), nullable=True),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['nation_id'], ['nation.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'settlementzone',
        sa.Column('nation_id', uuid_type, nullable=False),
        sa.Column('region_name', sa.String(), nullable=False),
        sa.Column('polygon_data', postgresql.JSONB(), nullable=False),
        sa.Column('color', sa.String(), nullable=True),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['nation_id'], ['nation.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'rolepermission',
        sa.Column('role_id', uuid_type, nullable=False),
        sa.Column('permission_id', uuid_type, nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permission.id']),
        sa.ForeignKeyConstraint(['role_id'], ['role.id']),
        sa.PrimaryKeyConstraint('role_id', 'permission_id'),
    )

    op.create_table(
        'userrole',
        sa.Column('user_id', uuid_type, nullable=False),
        sa.Column('role_id', uuid_type, nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['role.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
    )

    op.create_table(
        'gamequestion',
        sa.Column('game_id', uuid_type, nullable=False),
        sa.Column('question_text', sa.String(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['game_id'], ['game.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'gameoption',
        sa.Column('question_id', uuid_type, nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('explanation', sa.String(), nullable=True),
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['gamequestion.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('gameoption')
    op.drop_table('gamequestion')
    op.drop_table('userrole')
    op.drop_table('rolepermission')
    op.drop_table('settlementzone')
    op.drop_table('nationinfo')
    op.drop_table('game')
    op.drop_table('costume')
    op.drop_table('comment')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('permission')
    op.drop_index(op.f('ix_nation_slug'), table_name='nation')
    op.drop_index(op.f('ix_nation_name'), table_name='nation')
    op.drop_table('nation')

    postgresql.ENUM(name='gametype').drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name='gender').drop(op.get_bind(), checkfirst=True)
