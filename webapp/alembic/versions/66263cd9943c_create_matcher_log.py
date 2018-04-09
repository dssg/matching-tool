"""create matcher log

Revision ID: 66263cd9943c
Revises: 54bc94af6ead
Create Date: 2018-04-04 16:43:33.938060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66263cd9943c'
down_revision = '54bc94af6ead'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('match_log',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('upload_id', sa.String(length=255), nullable=True),
    sa.Column('match_start_timestamp', sa.DateTime(), nullable=True),
    sa.Column('match_complete_timestamp', sa.DateTime(), nullable=True),
    sa.Column('runtime', sa.Interval(), nullable=True),
    sa.ForeignKeyConstraint(['upload_id'], ['upload_log.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('match_log')
