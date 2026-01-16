#!/usr/bin/env python3
"""Script to create a test user in the database"""

import asyncio
import sys
import os
from datetime import datetime, timezone

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.database import create_db_and_tables, engine
from backend.src.models.user import UserCreate, User
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.src.auth.jwt import get_password_hash

async def create_test_user():
    # Create database tables
    await create_db_and_tables()
    
    # Create a test user
    user_data = UserCreate(
        email="aqsaarshi5@gmail.com",
        name="Aqsa Arshi",
        password="aqsa123"  # The password you're trying to use
    )
    
    async with AsyncSession(engine) as session:
        try:
            # Check if user already exists
            from sqlmodel import select
            existing_user = await session.exec(select(User).where(User.email == user_data.email))
            user_exists = existing_user.first()
            
            if user_exists:
                print(f"User {user_data.email} already exists.")
                return
            
            # Hash the password
            hashed_password = get_password_hash(user_data.password)
            
            # Create the user
            db_user = User(
                email=user_data.email,
                name=user_data.name,
                password_hash=hashed_password
            )
            
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            
            print(f"User created successfully: {db_user.email}")
            print(f"User ID: {db_user.id}")
        except ValueError as e:
            print(f"Error creating user: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(create_test_user())