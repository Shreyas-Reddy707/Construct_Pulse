"""add status to user

Revision ID: c76f68cb3c38
Revises: bfa04f480ce6
Create Date: 2026-06-03 16:07:06.378761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c76f68cb3c38'
down_revision: Union[str, Sequence[str], None] = 'bfa04f480ce6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    workerstatus = sa.Enum('PENDING', 'APPROVED', 'REJECTED', 'SUSPENDED', name='workerstatus')
    workerstatus.create(op.get_bind())
    op.add_column('users', sa.Column('status', workerstatus, nullable=True))
    op.execute("UPDATE users SET status = 'APPROVED' WHERE is_active = true")
    op.execute("UPDATE users SET status = 'PENDING' WHERE is_active = false")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'status')
    workerstatus = sa.Enum('PENDING', 'APPROVED', 'REJECTED', 'SUSPENDED', name='workerstatus')
    workerstatus.drop(op.get_bind())
