"""Add RBAC models

Revision ID: 39f6194fb2a7
Revises: 901cf362ff01
Create Date: 2026-07-03 16:18:47.494324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39f6194fb2a7'
down_revision: Union[str, Sequence[str], None] = '901cf362ff01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update UserRole enum outside transaction for PostgreSQL
    connection = op.get_bind()
    if connection.dialect.name == 'postgresql':
        connection.execution_options(isolation_level="AUTOCOMMIT")
        for new_role in ["Company Director", "Operations Manager", "Project Manager", "Site Manager", "Safety Officer", "Visitor"]:
            try:
                op.execute(f"ALTER TYPE userrole ADD VALUE IF NOT EXISTS '{new_role}'")
            except Exception:
                pass

    # Create tables
    op.create_table(
        'roles',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)

    op.create_table(
        'permission_groups',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permission_groups_name'), 'permission_groups', ['name'], unique=True)

    op.create_table(
        'permissions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_name'), 'permissions', ['name'], unique=True)

    op.create_table(
        'role_permission_group',
        sa.Column('role_id', sa.String(), nullable=False),
        sa.Column('permission_group_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['permission_group_id'], ['permission_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('role_id', 'permission_group_id')
    )

    op.create_table(
        'permission_group_permission',
        sa.Column('permission_group_id', sa.String(), nullable=False),
        sa.Column('permission_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['permission_group_id'], ['permission_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('permission_group_id', 'permission_id')
    )

    # Seed Data
    from sqlalchemy.sql import table, column
    import uuid

    roles_table = table('roles', column('id', sa.String), column('name', sa.String), column('description', sa.String))
    perm_groups_table = table('permission_groups', column('id', sa.String), column('name', sa.String), column('description', sa.String))
    perms_table = table('permissions', column('id', sa.String), column('name', sa.String), column('description', sa.String))
    rpg_table = table('role_permission_group', column('role_id', sa.String), column('permission_group_id', sa.String))
    pgp_table = table('permission_group_permission', column('permission_group_id', sa.String), column('permission_id', sa.String))

    # Roles
    roles = [
        {"id": str(uuid.uuid4()), "name": "System Admin", "description": "Platform Owner"},
        {"id": str(uuid.uuid4()), "name": "Company Director", "description": "Company Director"},
        {"id": str(uuid.uuid4()), "name": "Operations Manager", "description": "Operations Manager"},
        {"id": str(uuid.uuid4()), "name": "Company Admin", "description": "Company Administrator"},
        {"id": str(uuid.uuid4()), "name": "Project Manager", "description": "Project Manager"},
        {"id": str(uuid.uuid4()), "name": "Site Manager", "description": "Site Manager"},
        {"id": str(uuid.uuid4()), "name": "Safety Officer", "description": "Safety Officer"},
        {"id": str(uuid.uuid4()), "name": "Supervisor", "description": "Supervisor"},
        {"id": str(uuid.uuid4()), "name": "Worker", "description": "Worker"},
        {"id": str(uuid.uuid4()), "name": "Visitor", "description": "Visitor"},
    ]
    op.bulk_insert(roles_table, roles)

    # Permission Groups
    groups = [
        {"id": str(uuid.uuid4()), "name": "Attendance Group", "description": "Attendance permissions"},
        {"id": str(uuid.uuid4()), "name": "Workforce Group", "description": "Workforce permissions"},
        {"id": str(uuid.uuid4()), "name": "Assets Group", "description": "Assets permissions"},
        {"id": str(uuid.uuid4()), "name": "Safety Group", "description": "Safety permissions"}
    ]
    op.bulk_insert(perm_groups_table, groups)

    # Permissions
    permissions = [
        {"id": str(uuid.uuid4()), "name": "attendance.view", "description": "View attendance"},
        {"id": str(uuid.uuid4()), "name": "attendance.create", "description": "Create attendance"},
        {"id": str(uuid.uuid4()), "name": "attendance.edit", "description": "Edit attendance"},
        {"id": str(uuid.uuid4()), "name": "attendance.override", "description": "Override attendance"},
        {"id": str(uuid.uuid4()), "name": "attendance.export", "description": "Export attendance"},
        {"id": str(uuid.uuid4()), "name": "workforce.view", "description": "View workforce"},
        {"id": str(uuid.uuid4()), "name": "workforce.create", "description": "Create workforce"},
        {"id": str(uuid.uuid4()), "name": "workforce.update", "description": "Update workforce"},
        {"id": str(uuid.uuid4()), "name": "workforce.delete", "description": "Delete workforce"},
        {"id": str(uuid.uuid4()), "name": "assets.assign", "description": "Assign assets"},
        {"id": str(uuid.uuid4()), "name": "assets.inspect", "description": "Inspect assets"},
        {"id": str(uuid.uuid4()), "name": "assets.maintain", "description": "Maintain assets"},
        {"id": str(uuid.uuid4()), "name": "safety.report", "description": "Report safety"},
        {"id": str(uuid.uuid4()), "name": "safety.approve", "description": "Approve safety"},
        {"id": str(uuid.uuid4()), "name": "safety.close", "description": "Close safety"},
    ]
    op.bulk_insert(perms_table, permissions)

    # Mappings
    sys_admin_id = next(r["id"] for r in roles if r["name"] == "System Admin")
    
    rpg_mappings = [{"role_id": sys_admin_id, "permission_group_id": g["id"]} for g in groups]
    op.bulk_insert(rpg_table, rpg_mappings)

    pgp_mappings = []
    for p in permissions:
        if p["name"].startswith("attendance"):
            pgp_mappings.append({"permission_group_id": groups[0]["id"], "permission_id": p["id"]})
        elif p["name"].startswith("workforce"):
            pgp_mappings.append({"permission_group_id": groups[1]["id"], "permission_id": p["id"]})
        elif p["name"].startswith("assets"):
            pgp_mappings.append({"permission_group_id": groups[2]["id"], "permission_id": p["id"]})
        elif p["name"].startswith("safety"):
            pgp_mappings.append({"permission_group_id": groups[3]["id"], "permission_id": p["id"]})
            
    op.bulk_insert(pgp_table, pgp_mappings)


def downgrade() -> None:
    op.drop_table('permission_group_permission')
    op.drop_table('role_permission_group')
    op.drop_index(op.f('ix_permissions_name'), table_name='permissions')
    op.drop_table('permissions')
    op.drop_index(op.f('ix_permission_groups_name'), table_name='permission_groups')
    op.drop_table('permission_groups')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
    # Cannot reliably downgrade enums without complex postgres queries, leaving added enum values.
