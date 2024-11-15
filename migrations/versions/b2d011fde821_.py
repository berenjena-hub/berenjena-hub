"""empty message

Revision ID: b2d011fde821
Revises: 
Create Date: 2024-11-13 13:25:48.918936

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b2d011fde821'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notepad',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('follow', schema=None) as batch_op:
        batch_op.drop_index('_follower_followed_uc')
        batch_op.drop_column('followed_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('follow', schema=None) as batch_op:
        batch_op.add_column(sa.Column('followed_at', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=False))
        batch_op.create_index('_follower_followed_uc', ['follower_id', 'followed_id'], unique=True)

    op.drop_table('notepad')
    # ### end Alembic commands ###
