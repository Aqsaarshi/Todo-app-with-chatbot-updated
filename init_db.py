import asyncio
import sys
import os

# Add backend to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

from backend.src.database import create_db_and_tables

async def init_database():
    """Initialize the database and create tables"""
    print("Initializing database and creating tables...")
    await create_db_and_tables()
    print("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init_database())