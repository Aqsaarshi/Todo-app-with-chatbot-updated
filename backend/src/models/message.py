from sqlmodel import SQLModel, Field
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Dict, Any


class MessageBase(SQLModel):
    conversation_id: int
    sender_type: str  # 'user' or 'assistant'
    content: str
    message_metadata: Optional[Dict[str, Any]] = Field(sa_type=JSON)  # Using Field to specify JSON type


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    sender_type: str = Field(regex="^(user|assistant)$")  # 'user' or 'assistant'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_metadata: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    timestamp: datetime