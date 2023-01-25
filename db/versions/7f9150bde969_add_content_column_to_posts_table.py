"""add content column to posts table

Revision ID: 7f9150bde969
Revises: 06cc8589a19b
Create Date: 2023-01-09 16:36:45.716065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f9150bde969'
down_revision = '06cc8589a19b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
