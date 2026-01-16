from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .task import Task

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: str

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None