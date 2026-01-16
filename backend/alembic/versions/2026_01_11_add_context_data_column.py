"""Add context_data column to conversations table

Revision ID: abcdef123456
Revises: 1234567890ab
Create Date: 2026-01-11 20:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'abcdef123456'
down_revision = '1234567890ab'
branch_labels = None
depends_on = None


def upgrade():
    # Add context_data column to conversations table
    op.add_column('conversations', 
                  sa.Column('context_data', postgresql.JSON(astext_type=sa.Text()), nullable=True))


def downgrade():
    # Remove context_data column from conversations table
    op.drop_column('conversations', 'context_data')