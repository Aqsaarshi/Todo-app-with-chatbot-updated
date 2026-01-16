from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ChatRequest(BaseModel):
    """
    Model for chat request data
    """
    message: str = Field(..., min_length=1, max_length=1000, description="The message content from the user")
    conversation_id: Optional[str] = Field(None, description="ID of existing conversation, or None to start new")


class ChatResponse(BaseModel):
    """
    Model for chat response data
    """
    conversation_id: str
    response: str
    tool_calls: list
    timestamp: str


class ConversationsResponse(BaseModel):
    """
    Model for conversations response data
    """
    conversations: list
    total_count: int