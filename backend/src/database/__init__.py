from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from .config import DATABASE_URL
from ..models.user import User
from ..models.task import Task
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.tool_call import ToolCall

# Create the async database engine with proper connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300     # Recycle connections after 5 minutes
)

async def create_db_and_tables():
    """Create database tables for all models"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """Get an async database session"""
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()