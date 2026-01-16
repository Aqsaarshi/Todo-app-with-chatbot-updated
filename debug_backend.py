import sys
import os
import logging

# Set up logging to capture everything
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Add backend to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory to load env
os.chdir(backend_path)

print("Changed to backend directory:", os.getcwd())

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("Environment loaded.")
print("COHERE_API_KEY available:", bool(os.environ.get('COHERE_API_KEY')))

try:
    # Import the main app
    from src.main import app
    print("Main app imported successfully")
    
    # Import and test Cohere service
    from src.services.cohere_service import CohereService
    print("Cohere service module imported")
    
    service = CohereService()
    print("Cohere service instantiated successfully")
    
    # Test a simple response
    response = service.generate_response("Hello", max_tokens=20)
    print(f"Test response received: {response}")
    
except ImportError as ie:
    print(f"Import error: {ie}")
    import traceback
    traceback.print_exc()
except ValueError as ve:
    print(f"Value error (likely missing API key): {ve}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"General error: {e}")
    import traceback
    traceback.print_exc()