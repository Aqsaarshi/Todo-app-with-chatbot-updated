#!/usr/bin/env python3
"""Test script to debug the datetime issue in the User model"""

import asyncio
import sys
import os
from datetime import datetime, timezone

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.database import engine
from backend.src.models.user import User, UserCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.src.auth.jwt import get_password_hash

async def test_datetime_issue():
    print("Testing datetime issue...")
    
    # Create a test user
    user_data = UserCreate(
        email="test@example.com",
        name="Test User",
        password="testpassword"
    )
    
    async with AsyncSession(engine) as session:
        try:
            # Hash the password
            hashed_password = get_password_hash(user_data.password)
            
            # Create the user with explicit datetime handling
            db_user = User(
                email=user_data.email,
                name=user_data.name,
                password_hash=hashed_password
            )
            
            print(f"About to add user to session: {db_user}")
            session.add(db_user)
            print("Added user to session, committing...")
            await session.commit()
            print("Committed successfully!")
            await session.refresh(db_user)
            print(f"User created successfully: {db_user.email}")
            print(f"User ID: {db_user.id}")
        except Exception as e:
            print(f"Error creating user: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_datetime_issue())