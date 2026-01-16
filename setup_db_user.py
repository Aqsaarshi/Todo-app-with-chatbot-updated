import asyncio
import sys
import os
from uuid import UUID

# Add backend to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from backend.src.models.user import User
from backend.src.database.config import DATABASE_URL
from backend.src.auth.jwt import get_password_hash

# Create the async database engine
engine = create_async_engine(DATABASE_URL)

async def setup_database_and_user():
    """Initialize database and create default user if needed"""
    # First, create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    print("Database tables created successfully!")
    
    # Then, create the default user if it doesn't exist
    async with AsyncSession(engine) as session:
        user_id = "8e92c421-274b-439c-9101-13da389a8e4b"
        
        # Check if user already exists
        existing_user = await session.get(User, user_id)
        if existing_user:
            print(f"User {user_id} already exists in the database")
            return
        
        # Create a new user with the specific ID
        user = User(
            id=UUID(user_id),
            email="aqsaarshi5@gmail.com",
            name="Aqsa Arshi",
            password_hash=get_password_hash("defaultpassword")  # Use a default password hash
        )
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        print(f"Created user with ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Name: {user.name}")
        print("User created successfully!")

if __name__ == "__main__":
    asyncio.run(setup_database_and_user())