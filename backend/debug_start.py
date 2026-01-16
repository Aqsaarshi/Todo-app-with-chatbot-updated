import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment variables loaded.")
print(f"COHERE_API_KEY: {'SET' if os.getenv('COHERE_API_KEY') else 'NOT SET'}")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Attempting to import main app...")
    from src.main import app
    print("SUCCESS: Main app imported successfully!")
    
    # Check if chat router is included
    print("Checking routers...")
    for route in app.routes:
        if hasattr(route, 'path') and 'chat' in route.path:
            print(f"Found chat route: {route.path}")
    
except Exception as e:
    print(f"ERROR importing main app: {e}")
    import traceback
    traceback.print_exc()