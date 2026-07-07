"""Worker Identity Foundation

Revision ID: 92197f575aa5
Revises: 39f6194fb2a7
Create Date: 2026-07-03 18:37:00.600435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92197f575aa5'
down_revision: Union[str, Sequence[str], None] = '39f6194fb2a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add columns to users table
    op.add_column('users', sa.Column('designation', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove columns from users table
    op.drop_column('users', 'designation')
