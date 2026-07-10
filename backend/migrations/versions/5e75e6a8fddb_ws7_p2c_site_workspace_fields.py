"""ws7_p2c_site_workspace_fields

Revision ID: 5e75e6a8fddb
Revises: 92197f575aa5
Create Date: 2026-07-10 17:42:43.314693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5e75e6a8fddb'
down_revision: Union[str, Sequence[str], None] = '92197f575aa5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('sites', sa.Column('code', sa.String(), nullable=True))
    op.add_column('sites', sa.Column('municipality', sa.String(), nullable=True))
    op.add_column('sites', sa.Column('current_occupancy', sa.Integer(), server_default='0', nullable=False))
    op.add_column('sites', sa.Column('max_occupancy', sa.Integer(), server_default='0', nullable=False))
    op.add_column('sites', sa.Column('supervisor_name', sa.String(), nullable=True))
    op.add_column('sites', sa.Column('project_manager_id', sa.String(), nullable=True))
    
    op.create_foreign_key('fk_sites_project_manager_id_users', 'sites', 'users', ['project_manager_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_sites_project_manager_id_users', 'sites', type_='foreignkey')
    op.drop_column('sites', 'project_manager_id')
    op.drop_column('sites', 'supervisor_name')
    op.drop_column('sites', 'max_occupancy')
    op.drop_column('sites', 'current_occupancy')
    op.drop_column('sites', 'municipality')
    op.drop_column('sites', 'code')
