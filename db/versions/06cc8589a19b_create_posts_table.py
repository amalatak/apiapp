"""create posts table

Revision ID: 06cc8589a19b
Revises: 
Create Date: 2023-01-09 16:05:31.398078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06cc8589a19b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create post table
    op.create_table("posts", sa.Column("id", sa.INTEGER(), nullable=False, primary_key=True), 
        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
