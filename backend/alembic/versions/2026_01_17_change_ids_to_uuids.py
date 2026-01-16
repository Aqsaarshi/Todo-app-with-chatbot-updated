"""Change conversation and message IDs to UUIDs

Revision ID: 2026_01_17_change_ids_to_uuids
Revises: abcdef123456
Create Date: 2026-01-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '2026_01_17_change_ids_to_uuids'
down_revision = 'abcdef123456'
branch_labels = None
depends_on = None


def upgrade():
    # Create temporary columns with UUID type
    op.add_column('conversations', sa.Column('new_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.execute("UPDATE conversations SET new_id = gen_random_uuid()")
    op.alter_column('conversations', 'new_id', nullable=False)
    
    # Update foreign key in messages table
    op.add_column('messages', sa.Column('new_conversation_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.execute("""
        UPDATE messages 
        SET new_conversation_id = conversations.new_id 
        FROM conversations 
        WHERE messages.conversation_id = conversations.id
    """)
    op.alter_column('messages', 'new_conversation_id', nullable=False)
    
    # Update foreign key in tool_calls table
    op.add_column('tool_calls', sa.Column('new_message_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.execute("""
        UPDATE tool_calls 
        SET new_message_id = messages.new_id 
        FROM messages 
        WHERE tool_calls.message_id = messages.id
    """)
    op.alter_column('tool_calls', 'new_message_id', nullable=False)
    
    # Drop old foreign key constraints
    op.drop_constraint('tool_calls_message_id_fkey', 'tool_calls', type_='foreignkey')
    op.drop_constraint('messages_conversation_id_fkey', 'messages', type_='foreignkey')
    
    # Drop old primary key constraints
    op.drop_constraint('conversations_pkey', 'conversations', type_='primarykey')
    op.drop_constraint('messages_pkey', 'messages', type_='primarykey')
    op.drop_constraint('tool_calls_pkey', 'tool_calls', type_='primarykey')
    
    # Rename columns
    op.drop_column('conversations', 'id')
    op.alter_column('conversations', 'new_id', new_column_name='id', nullable=False)
    op.create_primary_key('conversations_pkey', 'conversations', ['id'])
    
    op.drop_column('messages', 'id')
    op.drop_column('messages', 'conversation_id')
    op.alter_column('messages', 'new_conversation_id', new_column_name='conversation_id', nullable=False)
    op.execute("ALTER TABLE messages ADD COLUMN new_id UUID DEFAULT gen_random_uuid()")
    op.alter_column('messages', 'new_id', new_column_name='id', nullable=False)
    op.create_primary_key('messages_pkey', 'messages', ['id'])
    op.create_foreign_key('messages_conversation_id_fkey', 'messages', 'conversations', ['conversation_id'], ['id'])
    
    op.drop_column('tool_calls', 'id')
    op.drop_column('tool_calls', 'message_id')
    op.alter_column('tool_calls', 'new_message_id', new_column_name='message_id', nullable=False)
    op.execute("ALTER TABLE tool_calls ADD COLUMN new_id UUID DEFAULT gen_random_uuid()")
    op.alter_column('tool_calls', 'new_id', new_column_name='id', nullable=False)
    op.create_primary_key('tool_calls_pkey', 'tool_calls', ['id'])
    op.create_foreign_key('tool_calls_message_id_fkey', 'tool_calls', 'messages', ['message_id'], ['id'])


def downgrade():
    # Reverse the changes - this is a complex operation that would require recreating the tables
    # For simplicity, we'll note that this migration is not easily reversible
    
    # This downgrade would be complex and potentially lose data, so we'll just document it
    # In practice, you'd want to backup your data before running this migration
    pass