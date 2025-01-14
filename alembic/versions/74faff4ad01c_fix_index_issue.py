"""Fix index issue

Revision ID: 74faff4ad01c
Revises: 4b2ad3886a86
Create Date: 2025-01-13 10:11:27.641042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74faff4ad01c'
down_revision: Union[str, None] = '4b2ad3886a86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('role', sa.Enum('guest', 'client', 'admin', name='role'), nullable=False))
    op.add_column('user_profile', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.create_index(op.f('ix_user_profile_user_id'), 'user_profile', ['user_id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_user_profile_user_id'), table_name='user_profile')
    op.drop_column('user_profile', 'is_verified')
    op.drop_column('user_profile', 'role')
    # ### end Alembic commands ###