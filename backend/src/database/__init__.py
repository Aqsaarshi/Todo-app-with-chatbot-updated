from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as SQLAlchemyAsyncSession
from .config import DATABASE_URL
from ..models.user import User
from ..models.task import Task

# Create the async database engine
engine = create_async_engine(DATABASE_URL, echo=True)

async def create_db_and_tables():
    """Create database tables for all models"""
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """Get an async database session"""
    async with AsyncSession(engine) as session:
        yield session