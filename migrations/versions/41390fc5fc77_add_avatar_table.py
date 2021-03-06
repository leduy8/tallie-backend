"""add Avatar table

Revision ID: 41390fc5fc77
Revises: 4c2277ed522b
Create Date: 2021-06-07 23:38:01.596007

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '41390fc5fc77'
down_revision = '4c2277ed522b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('avatar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('avatar')
    # ### end Alembic commands ###
