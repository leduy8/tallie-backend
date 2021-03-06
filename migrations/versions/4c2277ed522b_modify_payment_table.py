"""modify payment table

Revision ID: 4c2277ed522b
Revises: 5066f0f12ca3
Create Date: 2021-06-04 21:22:49.849188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c2277ed522b'
down_revision = '5066f0f12ca3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('card_number', sa.String(length=14), nullable=False))
    op.drop_column('payment', 'card_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('card_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('payment', 'card_number')
    # ### end Alembic commands ###
