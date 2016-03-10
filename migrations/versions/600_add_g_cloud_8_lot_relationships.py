""" G-Cloud 8 Lots

Revision ID: 600
Revises: 590
Create Date: 2016-03-10 10:00:01.000000

"""

# revision identifiers, used by Alembic.
revision = '600'
down_revision = '590'

from alembic import op


def upgrade():

    conn = op.get_bind()
    res = conn.execute("SELECT id FROM frameworks WHERE slug = 'g-cloud-8'")
    framework = list(res.fetchall())

    res = conn.execute("SELECT id FROM lots WHERE slug in ('saas', 'paas', 'iaas', 'scs')")
    lots = list(res.fetchall())

    if len(framework) == 0:
        raise Exception("Framework not found")

    for lot in lots:
        op.execute("INSERT INTO framework_lots (framework_id, lot_id) VALUES({}, {})".format(
            framework[0]["id"], lot["id"]))


def downgrade():
    conn = op.get_bind()
    res = conn.execute("SELECT id FROM frameworks WHERE slug = 'g-cloud-8'")
    framework = list(res.fetchall())

    op.execute("""
        DELETE FROM framework_lots WHERE framework_id={}
    """.format(framework[0]['id']))
