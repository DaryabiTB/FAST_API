"""adding  a column to post mode

Revision ID: a0c5640c61a7
Revises: c4eb83a6d3e7
Create Date: 2023-10-13 13:13:34.966312

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a0c5640c61a7'
down_revision = 'c4eb83a6d3e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
	op.drop_column('posts', 'content')
