"""Merge multiple heads into one

Revision ID: 7e20194c4ed5
Revises: 49f86c46dd69, 4a0a5ea70329, 9c9c1d6260de
Create Date: 2024-12-11 11:56:00.678076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e20194c4ed5'
down_revision = ('49f86c46dd69', '4a0a5ea70329', '9c9c1d6260de')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
