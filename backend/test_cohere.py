import sys
import os

# Add backend to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory to load env
os.chdir(backend_path)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("Environment loaded. Checking COHERE_API_KEY...")
cohere_key = os.environ.get('COHERE_API_KEY')
print(f"COHERE_API_KEY is {'SET' if cohere_key else 'NOT SET'}")

try:
    print("Attempting to import CohereService...")
    from src.services.cohere_service import CohereService
    
    print("Creating CohereService instance...")
    service = CohereService()
    print("CohereService created successfully!")
    
    print("Testing a simple generation...")
    response = service.generate_response("Say 'Hello, world!'")
    print(f"Response: {response}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()