import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('backend/.env')

# Print the COHERE_API_KEY
cohere_key = os.getenv('COHERE_API_KEY')
print(f"COHERE_API_KEY: {cohere_key}")

# Test Cohere service initialization
try:
    from backend.src.services.cohere_service import CohereService
    service = CohereService()
    print("Cohere service initialized successfully!")
except Exception as e:
    print(f"Error initializing Cohere service: {e}")