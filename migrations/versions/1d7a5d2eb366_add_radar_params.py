"""add radar params

Revision ID: 1d7a5d2eb366
Revises: e9adee2f247a
Create Date: 2020-06-11 16:10:05.315812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d7a5d2eb366'
down_revision = 'e9adee2f247a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('radar_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pri', sa.String(length=128), nullable=True),
    sa.Column('num_pulse', sa.String(length=128), nullable=True),
    sa.Column('range_samples', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('radar_parameters')
    # ### end Alembic commands ###
