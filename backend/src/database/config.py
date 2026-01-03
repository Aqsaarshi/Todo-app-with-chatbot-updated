import os
from dotenv import load_dotenv

load_dotenv()

# Use the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo.db")