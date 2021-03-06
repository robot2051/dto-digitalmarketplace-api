"""empty message

Revision ID: 6_service_role_abbreviations
Revises: 5_supplier_cascades
Create Date: 2016-07-25 11:41:53.011303

"""

# revision identifiers, used by Alembic.
revision = '6_service_role_abbreviations'
down_revision = '5_supplier_cascades'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from app import models
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_category', sa.Column('abbreviation', sa.String(length=15), nullable=True))
    op.add_column('service_role', sa.Column('abbreviation', sa.String(length=15), nullable=True))
    ### end Alembic commands ###
    categories = [
        ('Product Management', 'pm'),
        ('Business Analysis', 'ba'),
        ('Delivery Management and Agile Coaching', 'dm'),
        ('User Research', 'ur'),
        ('Service Design and Interaction Design', 'sd'),
        ('Technical Architecture, Development, Ethical Hacking and Web Operations', 'tech'),
        ('Performance and Web Analytics', 'wa'),
        ('Inclusive Design and Accessibility', 'acc'),
        ('Digital Transformation Advisors', 'dta'),
    ]
    for category in categories:
        SC = models.ServiceCategory.__table__
        op.execute(SC.update().\
                where(SC.c.name==op.inline_literal(category[0])).\
                values({'abbreviation': op.inline_literal(category[1])}))
    roles = [
        ('Junior Product Manager', 'pm-j'),
        ('Senior Product Manager', 'pm-s'),
        ('Junior Business Analyst', 'ba-j'),
        ('Senior Business Analyst', 'ba-s'),
        ('Junior Delivery Manager', 'dm-j'),
        ('Senior Delivery Manager', 'dm-s'),
        ('Senior Agile Coach', 'ac-s'),
        ('Senior User Research', 'ur-s'),
        ('Senior Service Designer', 'sd-s'),
        ('Junior Interaction Designer', 'id-j'),
        ('Senior Interaction Designer', 'id-s'),
        ('Senior Technical Lead', 'tl-s'),
        ('Junior Developer', 'dev-j'),
        ('Senior Developer', 'dev-s'),
        ('Junior Ethical Hacker', 'hack-j'),
        ('Senior Ethical Hacker', 'hack-s'),
        ('Junior Web Devops Engineer', 'devops-j'),
        ('Senior Web Devops Engineer', 'devops-s'),
        ('Junior Web Performance Analyst', 'wa-j'),
        ('Senior Web Performance Analyst', 'wa-s'),
        ('Junior Inclusive Designer (accessibility consultant)', 'id-j'),
        ('Senior Inclusive Designer (accessibility consultant)', 'id-s'),
        ('Senior Digital Transformation Advisor', 'dta-s'),
    ]
    for role in roles:
        SR = models.ServiceRole.__table__
        op.execute(SR.update().\
                where(SR.c.name==op.inline_literal(role[0])).\
                values({'abbreviation': op.inline_literal(role[1])}))


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service_role', 'abbreviation')
    op.drop_column('service_category', 'abbreviation')
    ### end Alembic commands ###
