"""ws7_p4c_department_workspace

Revision ID: 31ad79ac9318
Revises: 23124d14fc69
Create Date: 2026-07-10 22:25:04.843183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '31ad79ac9318'
down_revision: Union[str, Sequence[str], None] = '23124d14fc69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add Enum type
    department_status = postgresql.ENUM('ACTIVE', 'INACTIVE', name='departmentstatus')
    department_status.create(op.get_bind(), checkfirst=True)

    # 2. Add columns
    op.add_column('departments', sa.Column('department_code', sa.String(), nullable=True))
    op.add_column('departments', sa.Column('status', department_status, nullable=True))
    op.add_column('departments', sa.Column('department_head_id', sa.String(), nullable=True))
    op.add_column('departments', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('departments', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))

    # 3. Add FK and UniqueConstraint
    op.create_foreign_key('fk_departments_department_head_users', 'departments', 'users', ['department_head_id'], ['id'])
    op.create_unique_constraint('uq_company_department_code', 'departments', ['company_id', 'department_code'])

    # 4. Create explicitly required indexes
    op.create_index('ix_departments_department_code', 'departments', ['department_code'], unique=False)
    op.create_index('ix_departments_company_id', 'departments', ['company_id'], unique=False)
    op.create_index('ix_users_department_id', 'users', ['department_id'], unique=False)
    op.create_index('ix_department_to_site_department_id', 'department_to_site', ['department_id'], unique=False)


def downgrade() -> None:
    # 1. Drop explicit indexes
    op.drop_index('ix_department_to_site_department_id', table_name='department_to_site')
    op.drop_index('ix_users_department_id', table_name='users')
    op.drop_index('ix_departments_company_id', table_name='departments')
    op.drop_index('ix_departments_department_code', table_name='departments')
    
    # 2. Drop constraints
    op.drop_constraint('uq_company_department_code', 'departments', type_='unique')
    op.drop_constraint('fk_departments_department_head_users', 'departments', type_='foreignkey')
    
    # 3. Drop columns
    op.drop_column('departments', 'updated_at')
    op.drop_column('departments', 'created_at')
    op.drop_column('departments', 'department_head_id')
    op.drop_column('departments', 'status')
    op.drop_column('departments', 'department_code')
    
    # 4. Drop Enum
    department_status = postgresql.ENUM('ACTIVE', 'INACTIVE', name='departmentstatus')
    department_status.drop(op.get_bind(), checkfirst=True)
