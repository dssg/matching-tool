"""empty message

Revision ID: 54bc94af6ead
Revises: f60708767301
Create Date: 2017-12-26 16:10:22.054926

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '54bc94af6ead'
down_revision = 'f60708767301'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('upload_log', 'service_provider_slug', new_column_name='event_type_slug')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('upload_log', 'event_type_slug', new_column_name='service_provider_slug')
    # ### end Alembic commands ###
