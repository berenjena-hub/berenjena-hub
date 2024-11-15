"""empty message

Revision ID: 26b1ef13dc67
Revises: 5f21dffa2228
Create Date: 2024-11-13 13:27:24.393634

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '26b1ef13dc67'
down_revision = '5f21dffa2228'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('follow', schema=None) as batch_op:
        batch_op.drop_index('_follower_followed_uc')
        batch_op.drop_column('followed_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('follow', schema=None) as batch_op:
        batch_op.add_column(sa.Column('followed_at', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=False))
        batch_op.create_index('_follower_followed_uc', ['follower_id', 'followed_id'], unique=True)

    # ### end Alembic commands ###
