import requests
import json

print("Testing the chatbot functionality...")

BASE_URL = "http://127.0.0.1:8000"

# Test basic connectivity first
try:
    resp = requests.get(f"{BASE_URL}/health")
    print(f"Server health: {resp.status_code} - {resp.json()}")
except Exception as e:
    print(f"Server not accessible: {e}")
    exit()

# Try a simple test
print("\nTrying a simple test to see if the server responds...")

# Login to get a valid token
try:
    login_resp = requests.post(f"{BASE_URL}/api/auth/login?email=testuser3@example.com&password=securepassword123")
    print(f"Login response: {login_resp.status_code}")
    
    if login_resp.status_code == 200:
        login_data = login_resp.json()
        token = login_data['token']
        user_id = login_data['user_id']
        print("Login successful")
        
        # Try a simple request to see if we get any response
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Try with a simple message
        chat_payload = {
            "message": "hello",
            "conversation_id": None
        }
        
        chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
                                 headers=headers, 
                                 json=chat_payload)
        
        print(f"Simple message response status: {chat_resp.status_code}")
        if chat_resp.status_code == 200:
            print(f"Response: {chat_resp.json()}")
        else:
            print(f"Error response: {chat_resp.text}")
    else:
        print(f"Login failed: {login_resp.text}")
        
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()