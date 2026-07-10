"""ws7_p3c_contractor_workspace

Revision ID: 23124d14fc69
Revises: 5e75e6a8fddb
Create Date: 2026-07-10 21:09:02.028517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '23124d14fc69'
down_revision: Union[str, Sequence[str], None] = '5e75e6a8fddb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add Enum type for compliance_status
    contractor_compliance_status = postgresql.ENUM('COMPLIANT', 'NON_COMPLIANT', 'REVIEW_PENDING', name='contractorcompliancestatus')
    contractor_compliance_status.create(op.get_bind(), checkfirst=True)

    # 2. Add columns
    op.add_column('contractors', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('contractors', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('contractors', sa.Column('operational_status', sa.String(), nullable=True))
    op.add_column('contractors', sa.Column('compliance_status', contractor_compliance_status, nullable=True))
    op.add_column('contractors', sa.Column('contract_expiry', sa.DateTime(timezone=True), nullable=True))
    op.add_column('contractors', sa.Column('primary_contact_id', sa.String(), nullable=True))
    
    # 3. Create FK
    op.create_foreign_key('fk_contractors_primary_contact_users', 'contractors', 'users', ['primary_contact_id'], ['id'])
    
    # 4. Create explicit indexes
    op.create_index('ix_users_contractor_id', 'users', ['contractor_id'], unique=False)
    op.create_index('ix_users_contractor_active', 'users', ['contractor_id'], unique=False, postgresql_where=sa.text('is_active = true'))
    op.create_index('ix_contractor_to_site_contractor_id', 'contractor_to_site', ['contractor_id'], unique=False)


def downgrade() -> None:
    # 1. Drop explicit indexes
    op.drop_index('ix_contractor_to_site_contractor_id', table_name='contractor_to_site')
    op.drop_index('ix_users_contractor_active', table_name='users', postgresql_where=sa.text('is_active = true'))
    op.drop_index('ix_users_contractor_id', table_name='users')
    
    # 2. Drop FK
    op.drop_constraint('fk_contractors_primary_contact_users', 'contractors', type_='foreignkey')
    
    # 3. Drop columns
    op.drop_column('contractors', 'primary_contact_id')
    op.drop_column('contractors', 'contract_expiry')
    op.drop_column('contractors', 'compliance_status')
    op.drop_column('contractors', 'operational_status')
    op.drop_column('contractors', 'updated_at')
    op.drop_column('contractors', 'created_at')
    
    # 4. Drop Enum
    contractor_compliance_status = postgresql.ENUM('COMPLIANT', 'NON_COMPLIANT', 'REVIEW_PENDING', name='contractorcompliancestatus')
    contractor_compliance_status.drop(op.get_bind(), checkfirst=True)
