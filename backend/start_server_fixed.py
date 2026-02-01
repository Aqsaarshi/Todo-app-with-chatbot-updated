import asyncio
import uvicorn
import sys
import os

# Add backend to path
current_dir = os.getcwd()
sys.path.insert(0, current_dir)

# Load environment variables from current directory
from dotenv import load_dotenv
load_dotenv()

print("Environment loaded. Checking COHERE_API_KEY...")
cohere_key = os.environ.get('COHERE_API_KEY')
print(f"COHERE_API_KEY is {'SET' if cohere_key else 'NOT SET'}")

# Import the app after loading environment
from src.main import app

print("Starting server...")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True  # Enable auto-reload for development
    )