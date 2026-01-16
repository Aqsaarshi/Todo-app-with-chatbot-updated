from sqlmodel import SQLModel, Field
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Dict, Any


class ConversationBase(SQLModel):
    user_id: str
    title: Optional[str] = None


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    title: Optional[str] = None
    context_data: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)  # Store conversation context

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure updated_at is set to current time when initializing
        if 'updated_at' not in kwargs or kwargs['updated_at'] == self.updated_at:
            self.updated_at = datetime.utcnow()


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime