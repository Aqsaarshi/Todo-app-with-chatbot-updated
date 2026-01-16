from sqlmodel import Session
from typing import List
from datetime import datetime
from ..models.message import Message


def save_message(
    db_session: Session, 
    conversation_id: int, 
    sender_type: str, 
    content: str,
    metadata: dict = None
) -> Message:
    """
    Save a message to the database.
    
    Args:
        db_session: Database session
        conversation_id: ID of the conversation
        sender_type: Type of sender ('user' or 'assistant')
        content: Content of the message
        metadata: Optional metadata for the message
        
    Returns:
        Saved Message object
    """
    message = Message(
        conversation_id=conversation_id,
        sender_type=sender_type,
        content=content,
        message_metadata=metadata or {}
    )
    
    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)
    
    return message


def get_messages_for_conversation(
    db_session: Session, 
    conversation_id: int, 
    limit: int = 50, 
    offset: int = 0
) -> List[Message]:
    """
    Retrieve messages for a specific conversation.
    
    Args:
        db_session: Database session
        conversation_id: ID of the conversation
        limit: Number of messages to return
        offset: Number of messages to skip
        
    Returns:
        List of messages in chronological order
    """
    from sqlmodel import select
    
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.asc())
        .offset(offset)
        .limit(limit)
    )
    
    messages = db_session.exec(statement).all()
    
    return messages


def update_message_metadata(
    db_session: Session,
    message_id: int,
    metadata: dict
) -> Message:
    """
    Update the metadata for a specific message.
    
    Args:
        db_session: Database session
        message_id: ID of the message to update
        metadata: New metadata to set
        
    Returns:
        Updated Message object
    """
    message = db_session.get(Message, message_id)
    
    if not message:
        raise ValueError(f"Message with ID {message_id} not found")
    
    message.message_metadata = metadata
    message.timestamp = datetime.utcnow()  # Update timestamp when modifying
    
    db_session.add(message)
    db_session.commit()
    db_session.refresh(message)
    
    return message


def delete_message(db_session: Session, message_id: int) -> bool:
    """
    Delete a message from the database.
    
    Args:
        db_session: Database session
        message_id: ID of the message to delete
        
    Returns:
        True if message was deleted, False if not found
    """
    message = db_session.get(Message, message_id)
    
    if not message:
        return False
    
    db_session.delete(message)
    db_session.commit()
    
    return True