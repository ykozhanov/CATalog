"""Initial migration

Revision ID: e9086a49e1f0
Revises: 
Create Date: 2025-03-05 14:09:42.040584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9086a49e1f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('telegram_user_id', sa.Integer(), nullable=False),
    sa.Column('access_jtw_token', sa.String(), nullable=False),
    sa.Column('refresh_jtw_token', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('telegram_user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
