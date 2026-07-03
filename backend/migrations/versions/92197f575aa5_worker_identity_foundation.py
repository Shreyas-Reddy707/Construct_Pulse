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
    op.add_column('users', sa.Column('emergency_contact_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('emergency_contact_phone', sa.String(), nullable=True))
    op.add_column('users', sa.Column('emergency_contact_relationship', sa.String(), nullable=True))

    # Move data from sessions to users (preserve data)
    op.execute('''
        UPDATE users
        SET emergency_contact_name = s.emergency_contact_name,
            emergency_contact_phone = s.emergency_contact_phone,
            emergency_contact_relationship = s.emergency_contact_relationship
        FROM (
            SELECT DISTINCT ON (user_id) user_id, emergency_contact_name, emergency_contact_phone, emergency_contact_relationship
            FROM sessions
            WHERE emergency_contact_name IS NOT NULL OR emergency_contact_phone IS NOT NULL
            ORDER BY user_id, login_time DESC
        ) AS s
        WHERE users.id = s.user_id
    ''')

    # Remove columns from sessions table
    op.drop_column('sessions', 'emergency_contact_name')
    op.drop_column('sessions', 'emergency_contact_phone')
    op.drop_column('sessions', 'emergency_contact_relationship')


def downgrade() -> None:
    # Add columns back to sessions table
    op.add_column('sessions', sa.Column('emergency_contact_relationship', sa.String(), nullable=True))
    op.add_column('sessions', sa.Column('emergency_contact_phone', sa.String(), nullable=True))
    op.add_column('sessions', sa.Column('emergency_contact_name', sa.String(), nullable=True))

    # Move data back to sessions
    op.execute('''
        UPDATE sessions
        SET emergency_contact_name = u.emergency_contact_name,
            emergency_contact_phone = u.emergency_contact_phone,
            emergency_contact_relationship = u.emergency_contact_relationship
        FROM users u
        WHERE sessions.user_id = u.id
    ''')

    # Remove columns from users table
    op.drop_column('users', 'emergency_contact_relationship')
    op.drop_column('users', 'emergency_contact_phone')
    op.drop_column('users', 'emergency_contact_name')
    op.drop_column('users', 'designation')
