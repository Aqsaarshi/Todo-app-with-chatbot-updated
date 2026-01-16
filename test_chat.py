import requests
import json
from uuid import UUID

# Test the chat endpoint
BASE_URL = "http://127.0.0.1:8000"

# First, let's try to register a test user
print("Creating a test user...")

# Register a new user
register_data = {
    "email": "testuser@example.com",
    "name": "Test User",
    "password": "securepassword123"
}

try:
    register_resp = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print(f"Registration response: {register_resp.status_code}")
    if register_resp.status_code == 200:
        register_data = register_resp.json()
        print(f"Registration success: {register_data}")
        token = register_data['token']
        user_id = register_data['user_id']
        print(f"User ID: {user_id}")
        
        # Now try to use the chat endpoint
        print(f"\nTrying to access chat endpoint with user ID: {user_id}")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        chat_payload = {
            "message": "Hello, I want to add a task called 'driving'",
            "conversation_id": None
        }
        
        # Try the chat endpoint
        chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
                                 headers=headers, 
                                 json=chat_payload)
        
        print(f"Chat response status: {chat_resp.status_code}")
        print(f"Chat response: {chat_resp.text}")
        
    else:
        print(f"Registration failed: {register_resp.text}")
        
except Exception as e:
    print(f"Error during test: {e}")