import requests
import json

# Test the chat endpoint on the Hugging Face Space
BASE_URL = "https://aqsaarshi-todo-app-with-chatbot.hf.space"

# First, let's register a test user
print("Creating a test user on Hugging Face Space...")

# Register a new user
import uuid
test_email = f"testuser_{uuid.uuid4()}@example.com"
register_data = {
    "email": test_email,
    "name": "Test User",
    "password": "securepassword123"
}

try:
    register_resp = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print(f"Registration response: {register_resp.status_code}")
    if register_resp.status_code == 200:
        register_data = register_resp.json()
        print(f"Registration success: User ID received")
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
            "message": "create task test driving on Hugging Face",
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
    print("This might be expected if rate limits are in place on the Hugging Face Space")