"""increase a limit for username

Revision ID: f31305f1b05a
Revises: 3dbfc45efd5f
Create Date: 2024-04-25 21:24:59.174697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f31305f1b05a'
down_revision: Union[str, None] = '3dbfc45efd5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###
