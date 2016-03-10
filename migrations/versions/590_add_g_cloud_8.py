""" G-Cloud 8

Revision ID: 590
Revises: 580
Create Date: 2016-03-10 10:00:00.000000

"""

# revision identifiers, used by Alembic.
revision = '590'
down_revision = '580'

from alembic import op


def upgrade():

    conn = op.get_bind()
    res = conn.execute("SELECT * FROM frameworks WHERE slug = 'g-cloud-8'")
    results = res.fetchall()

    if not results:
        op.execute("""
            INSERT INTO frameworks (name, framework, status, slug, clarification_questions_open)
                values('G-Cloud 8', 'g-cloud', 'open', 'g-cloud-8', TRUE)
        """)


def downgrade():
    op.execute("""
        DELETE FROM frameworks where slug='g-cloud-8'
    """)
