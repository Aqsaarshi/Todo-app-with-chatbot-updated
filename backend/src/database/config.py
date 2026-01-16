import os
from dotenv import load_dotenv

load_dotenv()

# Use the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo.db")

# If using PostgreSQL, ensure it uses the async driver
if DATABASE_URL.startswith("postgresql://"):
    # Replace postgresql:// with postgresql+asyncpg:// and remove SSL parameters
    # asyncpg handles SSL differently and doesn't accept sslmode in the URL
    base_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    # Remove sslmode and channel_binding parameters as they're not supported by asyncpg in the URL
    if "?sslmode=require&channel_binding=require" in base_url:
        base_url = base_url.replace("?sslmode=require&channel_binding=require", "")
    elif "?sslmode=require" in base_url:
        base_url = base_url.replace("?sslmode=require", "")
    DATABASE_URL = base_url
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    # Remove sslmode and channel_binding parameters as they're not supported by asyncpg in the URL
    if "?sslmode=require&channel_binding=require" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("?sslmode=require&channel_binding=require", "")
    elif "?sslmode=require" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("?sslmode=require", "")
elif DATABASE_URL.startswith("postgresql+asyncpg://"):
    # If already in the correct format, use as is
    DATABASE_URL = DATABASE_URL