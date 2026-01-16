"""Add chatbot tables

Revision ID: 1234567890ab
Revises: 001_initial
Create Date: 2026-01-10 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '1234567890ab'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    # Create conversations table
    op.create_table('conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_user_id'), 'conversations', ['user_id'], unique=False)

    # Create messages table
    op.create_table('messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('sender_type', sa.String(), nullable=False),
        sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)

    # Create tool_calls table
    op.create_table('tool_calls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.Column('tool_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('result', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('executed_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop tool_calls table
    op.drop_table('tool_calls')
    
    # Drop messages table
    op.drop_index(op.f('ix_messages_conversation_id'), table_name='messages')
    op.drop_table('messages')
    
    # Drop conversations table
    op.drop_index(op.f('ix_conversations_user_id'), table_name='conversations')
    op.drop_table('conversations')