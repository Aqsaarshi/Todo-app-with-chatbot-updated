from sqlmodel import SQLModel, Field
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Dict, Any


class ToolCallBase(SQLModel):
    message_id: int
    tool_name: str
    parameters: Dict[str, Any] = Field(sa_type=JSON)
    result: Optional[Dict[str, Any]] = Field(sa_type=JSON)


class ToolCall(ToolCallBase, table=True):
    __tablename__ = "tool_calls"

    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key="messages.id")
    tool_name: str
    parameters: Dict[str, Any] = Field(default={}, sa_type=JSON)
    result: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)
    executed_at: datetime = Field(default_factory=datetime.utcnow)


class ToolCallCreate(ToolCallBase):
    pass


class ToolCallRead(ToolCallBase):
    id: int
    executed_at: datetime