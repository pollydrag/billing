"""init

Revision ID: ab9cf9075871
Revises: 
Create Date: 2020-04-08 12:16:08.326294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab9cf9075871'
down_revision = 'init'
branch_labels = None
depends_on = None

INIT_FILE = './migrations/versions/init_schema.sql'

TABLES = [
    'history',
    'wallets',
    'clients',
]

TYPES = [
    'currency_enum'
]

def upgrade():
    with open(INIT_FILE, 'r') as f:
        op.execute(f.read())


def downgrade():
    conn = op.get_bind()

    for table in TABLES:
        conn.execute(f'DROP TABLE {table} CASCADE ')

    # for type_ in TYPES:
    #     conn.execute(f'DROP TYPE {type_}')
