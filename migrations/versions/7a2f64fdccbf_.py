# Revision ID: a8ef68b8dd4d
# Revises:
# Create Date: 2024-12-11 21:27:15.996678

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a8ef68b8dd4d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # No se necesita eliminar el índice _follower_followed_uc en esta migración
    pass

def downgrade():
    with op.batch_alter_table('follow', schema=None) as batch_op:
        # Volvemos a crear el índice ya que se necesita para la relación clave foránea
        batch_op.create_index('_follower_followed_uc', ['follower_id', 'followed_id'], unique=True)
