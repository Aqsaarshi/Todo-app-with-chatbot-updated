import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

# Change to backend directory to load env
backend_dir = os.path.join(os.getcwd(), 'backend')
os.chdir(backend_dir)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("Current working directory:", os.getcwd())
print("Environment variables loaded.")

# Check if COHERE_API_KEY is available
cohere_key = os.environ.get('COHERE_API_KEY')
print(f"COHERE_API_KEY available: {'Yes' if cohere_key else 'No'}")

# Try to import and initialize the app
try:
    from src.main import app
    print("App imported successfully")
    
    # Try to initialize Cohere service
    from src.services.cohere_service import CohereService
    service = CohereService()
    print("Cohere service initialized successfully")
    
    # Test a simple response
    response = service.generate_response("Hello")
    print(f"Test response: {response[:50]}...")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()