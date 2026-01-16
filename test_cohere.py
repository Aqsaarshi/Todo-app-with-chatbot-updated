import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv('backend/.env')

# Add backend to Python path
sys.path.insert(0, 'backend')

from backend.src.services.cohere_service import CohereService

try:
    cohere_service = CohereService()
    print("Cohere service initialized successfully")
    
    # Test a simple prompt
    test_prompt = "Say hello"
    response = cohere_service.generate_response(test_prompt)
    print(f"Response: {response}")
    
except Exception as e:
    print(f"Error initializing Cohere service: {e}")
    import traceback
    traceback.print_exc()