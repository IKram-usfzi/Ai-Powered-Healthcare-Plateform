"""add weight_kg to health_readings

Revision ID: add_weight_kg
Revises: c166687b21e9
Create Date: 2026-09-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_weight_kg'
down_revision = 'c166687b21e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('health_readings', sa.Column('weight_kg', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('health_readings', 'weight_kg')
