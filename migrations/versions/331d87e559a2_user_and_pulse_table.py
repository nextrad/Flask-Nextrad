"""user and pulse table

Revision ID: 331d87e559a2
Revises: 
Create Date: 2020-06-10 20:38:17.919335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '331d87e559a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pulse',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('frequency', sa.String(length=64), nullable=True),
    sa.Column('polarisation', sa.String(length=64), nullable=True),
    sa.Column('pulse_width', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pulse_frequency'), 'pulse', ['frequency'], unique=True)
    op.create_index(op.f('ix_pulse_polarisation'), 'pulse', ['polarisation'], unique=True)
    op.create_index(op.f('ix_pulse_pulse_width'), 'pulse', ['pulse_width'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_pulse_pulse_width'), table_name='pulse')
    op.drop_index(op.f('ix_pulse_polarisation'), table_name='pulse')
    op.drop_index(op.f('ix_pulse_frequency'), table_name='pulse')
    op.drop_table('pulse')
    # ### end Alembic commands ###
