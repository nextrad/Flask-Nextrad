"""add init

Revision ID: 4d50dd107ae4
Revises: 79bf0d8f84c3
Create Date: 2020-06-10 23:18:20.647091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d50dd107ae4'
down_revision = '79bf0d8f84c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_pulse_frequency', table_name='pulse')
    op.drop_index('ix_pulse_polarisation', table_name='pulse')
    op.drop_index('ix_pulse_pulse_width', table_name='pulse')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_pulse_pulse_width', 'pulse', ['pulse_width'], unique=False)
    op.create_index('ix_pulse_polarisation', 'pulse', ['polarisation'], unique=False)
    op.create_index('ix_pulse_frequency', 'pulse', ['frequency'], unique=False)
    # ### end Alembic commands ###
