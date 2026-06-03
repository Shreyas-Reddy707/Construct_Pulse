"""p1_backfill_company_ids

Revision ID: ba7c116860f4
Revises: 1bfd7ef2246b
Create Date: 2026-06-03 23:21:14.555201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba7c116860f4'
down_revision: Union[str, Sequence[str], None] = '1bfd7ef2246b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First ensure demo_company exists
    conn = op.get_bind()
    res = conn.execute(sa.text("SELECT id FROM companies WHERE id = 'demo_company'"))
    demo_exists = res.fetchone()
    
    if demo_exists:
        op.execute("UPDATE users SET company_id = 'demo_company' WHERE company_id IS NULL")
        op.execute("UPDATE departments SET company_id = 'demo_company' WHERE company_id IS NULL")
        op.execute("UPDATE contractors SET company_id = 'demo_company' WHERE company_id IS NULL")
        op.execute("UPDATE attendances SET company_id = 'demo_company' WHERE company_id IS NULL")


def downgrade() -> None:
    """Downgrade schema."""
    pass
