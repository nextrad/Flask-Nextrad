"""add pri

Revision ID: e9adee2f247a
Revises: 4d50dd107ae4
Create Date: 2020-06-11 14:26:09.299537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9adee2f247a'
down_revision = '4d50dd107ae4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pulse', sa.Column('pri', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pulse', 'pri')
    # ### end Alembic commands ###
