"""update abuse, helpful table

Revision ID: 87c1ac1347ff
Revises: cb9bc56ee383
Create Date: 2021-06-14 21:37:48.296218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87c1ac1347ff'
down_revision = 'cb9bc56ee383'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('abuse', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'abuse', 'user', ['user_id'], ['id'])
    op.add_column('helpful', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'helpful', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'helpful', type_='foreignkey')
    op.drop_column('helpful', 'user_id')
    op.drop_constraint(None, 'abuse', type_='foreignkey')
    op.drop_column('abuse', 'user_id')
    # ### end Alembic commands ###
