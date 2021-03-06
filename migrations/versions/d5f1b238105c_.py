"""empty message

Revision ID: d5f1b238105c
Revises: 1_price_schedule_data
Create Date: 2016-07-21 16:44:23.264457

"""

# revision identifiers, used by Alembic.
revision = 'd5f1b238105c'
down_revision = '1_price_schedule_data'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('address', 'address_line',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('address', 'suburb',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('contact', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('price_schedule', 'daily_rate',
               existing_type=sa.NUMERIC(),
               nullable=True)
    op.alter_column('price_schedule', 'hourly_rate',
               existing_type=sa.NUMERIC(),
               nullable=True)
    op.alter_column('supplier_reference', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('supplier_reference', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('price_schedule', 'hourly_rate',
               existing_type=sa.NUMERIC(),
               nullable=False)
    op.alter_column('price_schedule', 'daily_rate',
               existing_type=sa.NUMERIC(),
               nullable=False)
    op.alter_column('contact', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('address', 'suburb',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('address', 'address_line',
               existing_type=sa.VARCHAR(),
               nullable=False)
    ### end Alembic commands ###
