import asyncio
import uvicorn
import sys
import os

# Change to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Add the backend directory to the path
backend_path = os.path.join(script_dir, 'backend')
sys.path.insert(0, backend_path)

# Load environment variables from the backend directory
env_path = os.path.join(backend_path, '.env')
from dotenv import load_dotenv
load_dotenv(env_path)

print("Environment loaded. Checking COHERE_API_KEY...")
cohere_key = os.environ.get('COHERE_API_KEY')
print(f"COHERE_API_KEY is {'SET' if cohere_key else 'NOT SET'}")

# Import the app after loading environment
os.chdir(backend_path)  # Ensure we're in the backend directory for imports
from src.main import app

print("Starting server...")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )