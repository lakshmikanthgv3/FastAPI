"""Create Phone number for user table

Revision ID: 2c347548b3e4
Revises:
Create Date: 2024-12-27 09:24:42.450901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c347548b3e4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('Phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'Phone_number')
