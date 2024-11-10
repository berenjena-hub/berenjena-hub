"""create_notepad_model

Revision ID: 8f54ad2d07e9
Revises: b70062d4ef9d
Create Date: 2024-11-10 01:23:52.363964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f54ad2d07e9'
down_revision = 'b70062d4ef9d'
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notepad')
    # ### end Alembic commands ###
