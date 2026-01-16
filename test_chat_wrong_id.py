import requests
import json
from uuid import UUID

# Test the chat endpoint with the user ID from the logs
BASE_URL = "http://127.0.0.1:8000"

# Use the user ID from the logs: 8e92c421-274b-439c-9101-13da389a8e4b
user_id_from_logs = "8e92c421-274b-439c-9101-13da389a8e4b"

# First, let's try to login with an existing user to get a valid token
print("Logging in to get a valid token...")

login_data = {
    "email": "testuser@example.com",
    "password": "securepassword123"
}

try:
    login_resp = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    print(f"Login response: {login_resp.status_code}")
    
    if login_resp.status_code == 200:
        login_data = login_resp.json()
        print(f"Login success: {login_data}")
        token = login_data['token']
        actual_user_id = login_data['user_id']
        print(f"Actual User ID from token: {actual_user_id}")
        print(f"User ID from logs: {user_id_from_logs}")
        
        # Check if these UUIDs are equal
        try:
            uuid1 = UUID(actual_user_id)
            uuid2 = UUID(user_id_from_logs)
            print(f"Are UUIDs equal? {uuid1 == uuid2}")
        except ValueError as e:
            print(f"Error parsing UUIDs: {e}")
        
        # Now try to use the chat endpoint with the user ID from logs (which should fail)
        print(f"\nTrying to access chat endpoint with user ID from logs: {user_id_from_logs}")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        chat_payload = {
            "message": "Hello, I want to add a task called 'driving'",
            "conversation_id": None
        }
        
        # Try the chat endpoint with the wrong user ID
        chat_resp = requests.post(f"{BASE_URL}/api/{user_id_from_logs}/chat", 
                                 headers=headers, 
                                 json=chat_payload)
        
        print(f"Chat response status: {chat_resp.status_code}")
        print(f"Chat response: {chat_resp.text}")
        
        # Now try with the correct user ID
        print(f"\nTrying to access chat endpoint with correct user ID: {actual_user_id}")
        chat_resp_correct = requests.post(f"{BASE_URL}/api/{actual_user_id}/chat", 
                                         headers=headers, 
                                         json=chat_payload)
        
        print(f"Correct Chat response status: {chat_resp_correct.status_code}")
        print(f"Correct Chat response: {chat_resp_correct.text}")
        
    else:
        print(f"Login failed: {login_resp.text}")
        
except Exception as e:
    print(f"Error during test: {e}")