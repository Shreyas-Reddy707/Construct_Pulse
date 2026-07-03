"""Add Session model and Platform Owner seed

Revision ID: 901cf362ff01
Revises: 70b43e86330a
Create Date: 2026-07-03 14:05:56.052156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '901cf362ff01'
down_revision: Union[str, Sequence[str], None] = '70b43e86330a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('device_id', sa.String(), nullable=True),
        sa.Column('device_name', sa.String(), nullable=True),
        sa.Column('device_platform', sa.String(), nullable=True),
        sa.Column('app_version', sa.String(), nullable=True),
        sa.Column('login_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_activity', sa.DateTime(timezone=True), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('push_token', sa.String(), nullable=True),
        sa.Column('is_revoked', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Seed Platform Owner
    op.execute(
        "INSERT INTO users (id, phone_number, firebase_uid, name, role, is_active, status, is_deleted) "
        "VALUES ('00000000-0000-0000-0000-000000000000', '+10000000000', 'firebase_platform_owner', 'Platform Owner', 'SYSTEM_ADMIN'::userrole, true, 'APPROVED'::workerstatus, false) "
        "ON CONFLICT (id) DO NOTHING"
    )


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE id = '00000000-0000-0000-0000-000000000000'")
    op.drop_table('sessions')
