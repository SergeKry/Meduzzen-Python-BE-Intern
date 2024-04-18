"""add salt column for users

Revision ID: 1e1372e10411
Revises: 3dbfc45efd5f
Create Date: 2024-04-18 19:28:38.525881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e1372e10411'
down_revision: Union[str, None] = '3dbfc45efd5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('salt', sa.LargeBinary(), nullable=True))
    op.drop_column('users', 'password')


def downgrade() -> None:
    op.drop_column('users', 'salt')
