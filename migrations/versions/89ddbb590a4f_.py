"""empty message

Revision ID: 89ddbb590a4f
Revises: a4f17e7db43b
Create Date: 2016-07-19 15:20:21.405951

"""

# revision identifiers, used by Alembic.
revision = '89ddbb590a4f'
down_revision = 'a4f17e7db43b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['service_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price_schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('supplier_id', sa.Integer(), nullable=False),
    sa.Column('service_role_id', sa.Integer(), nullable=False),
    sa.Column('hourly_rate', sa.Numeric(), nullable=False),
    sa.Column('daily_rate', sa.Numeric(), nullable=False),
    sa.Column('gst_included', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['service_role_id'], ['service_role.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('price_schedule')
    op.drop_table('service_role')
    ### end Alembic commands ###
