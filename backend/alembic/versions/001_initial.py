"""Initial migration

Revision ID: 001_initial
Revises:
Create Date: 2025-12-27 22:45:00

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table('user',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create tasks table
    op.create_table('task',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('priority', sa.String(), nullable=False),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_task_user_id', 'task', ['user_id'])
    op.create_index('ix_task_user_id_completed', 'task', ['user_id', 'completed'])
    op.create_index('ix_task_user_id_priority', 'task', ['user_id', 'priority'])
    op.create_index('ix_task_user_id_due_date', 'task', ['user_id', 'due_date'])
    op.create_index('ix_task_user_id_created_at', 'task', ['user_id', 'created_at'])
    op.create_index('ix_task_completed', 'task', ['completed'])
    op.create_index('ix_task_priority', 'task', ['priority'])
    op.create_index('ix_task_due_date', 'task', ['due_date'])


def downgrade():
    op.drop_index('ix_task_due_date', table_name='task')
    op.drop_index('ix_task_priority', table_name='task')
    op.drop_index('ix_task_completed', table_name='task')
    op.drop_index('ix_task_user_id_created_at', table_name='task')
    op.drop_index('ix_task_user_id_due_date', table_name='task')
    op.drop_index('ix_task_user_id_priority', table_name='task')
    op.drop_index('ix_task_user_id_completed', table_name='task')
    op.drop_index('ix_task_user_id', table_name='task')

    op.drop_table('task')
    op.drop_table('user')