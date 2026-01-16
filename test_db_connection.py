import os
import sys
from dotenv import load_dotenv

# Add backend to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

load_dotenv()

# Import the database config after loading env vars
from backend.src.database.config import DATABASE_URL

print(f"DATABASE_URL: {DATABASE_URL}")

# Test importing the database module
try:
    from backend.src.database import engine
    print("Successfully imported database engine!")
    print(f"Engine dialect: {engine.dialect.name}")
except Exception as e:
    print(f"Error importing database engine: {e}")