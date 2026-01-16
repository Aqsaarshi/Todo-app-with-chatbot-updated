import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv('backend/.env')

# Add backend to Python path
sys.path.insert(0, 'backend')

# Import and run the app
from backend.src.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)