"""create post table

Revision ID: c4eb83a6d3e7
Revises: 6a000537b225
Create Date: 2023-10-13 12:40:50.403805

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c4eb83a6d3e7'
down_revision = '6a000537b225'
branch_labels = None
depends_on = None


def upgrade() -> None:
	op.create_table('Posts', sa.Column('id', sa.Integer, primary_key=True, nullable=False),
	                sa.Column('title', sa.String, nullable=False))


def downgrade() -> None:
	op.drop_table('Posts')
