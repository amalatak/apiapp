"""add last few columnts

Revision ID: 55ad6a4e6d32
Revises: 6c83938adb61
Create Date: 2023-01-09 17:04:58.404453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55ad6a4e6d32'
down_revision = '6c83938adb61'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('')
    pass


def downgrade() -> None:
    pass
