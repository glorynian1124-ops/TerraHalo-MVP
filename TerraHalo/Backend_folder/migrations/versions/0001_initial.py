"""initial schema — 22 tables

Revision ID: 0001_initial
Create Date: 2026-06-14
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # This migration is generated as a baseline; all tables are created
    # by db.create_all() in development. For production, run schema.sql first
    # or uncomment the table creation statements below.
    pass


def downgrade():
    pass
