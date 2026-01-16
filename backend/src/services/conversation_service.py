from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Dict, Any
from ..models.conversation import Conversation
from ..models.message import Message


async def get_conversation_history(db_session: AsyncSession, conversation_id: int) -> List[Message]:
    """
    Retrieve the history of messages for a specific conversation.

    Args:
        db_session: Database session
        conversation_id: ID of the conversation to retrieve history for

    Returns:
        List of messages in chronological order
    """
    # Query messages for the conversation, ordered by timestamp
    # Using a more efficient query with explicit joins if needed
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.asc())
    )

    result = await db_session.exec(statement)
    messages = result.all()

    return messages


async def get_conversation_context(db_session: AsyncSession, conversation_id: int) -> Dict[str, Any]:
    """
    Retrieve the context data for a specific conversation.

    Args:
        db_session: Database session
        conversation_id: ID of the conversation to retrieve context for

    Returns:
        Dictionary containing conversation context data
    """
    conversation = await db_session.get(Conversation, conversation_id)

    if not conversation:
        raise ValueError(f"Conversation {conversation_id} not found")

    return conversation.context_data or {}


async def update_conversation_context(db_session: AsyncSession, conversation_id: int, context_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the context data for a specific conversation.

    Args:
        db_session: Database session
        conversation_id: ID of the conversation to update
        context_data: New context data to merge with existing context

    Returns:
        Updated context data
    """
    conversation = await db_session.get(Conversation, conversation_id)

    if not conversation:
        raise ValueError(f"Conversation {conversation_id} not found")

    # Merge the new context data with existing context
    existing_context = conversation.context_data or {}
    updated_context = {**existing_context, **context_data}

    conversation.context_data = updated_context
    db_session.add(conversation)
    await db_session.commit()
    await db_session.refresh(conversation)

    return conversation.context_data


async def get_user_conversations(db_session: AsyncSession, user_id: str) -> List[Conversation]:
    """
    Retrieve all conversations for a specific user.

    Args:
        db_session: Database session
        user_id: ID of the user

    Returns:
        List of user's conversations
    """
    statement = select(Conversation).where(Conversation.user_id == user_id)
    result = await db_session.exec(statement)
    conversations = result.all()

    return conversations


async def get_conversation_by_id(db_session: AsyncSession, conversation_id: int, user_id: str) -> Conversation:
    """
    Retrieve a specific conversation by ID for a user.

    Args:
        db_session: Database session
        conversation_id: ID of the conversation
        user_id: ID of the user

    Returns:
        Conversation object if found and belongs to user

    Raises:
        ValueError: If conversation doesn't exist or doesn't belong to user
    """
    conversation = await db_session.get(Conversation, conversation_id)

    if not conversation or conversation.user_id != user_id:
        raise ValueError(f"Conversation {conversation_id} not found or does not belong to user {user_id}")

    return conversation