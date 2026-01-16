import requests
import json

print("Testing the chatbot task functionality...")

BASE_URL = "http://127.0.0.1:8000"

# Login to get a valid token
try:
    login_resp = requests.post(f"{BASE_URL}/api/auth/login?email=testuser3@example.com&password=securepassword123")
    print(f"Login response: {login_resp.status_code}")
    
    if login_resp.status_code == 200:
        login_data = login_resp.json()
        token = login_data['token']
        user_id = login_data['user_id']
        print("Login successful")
        
        # Test with "add task cooking"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print("\nTesting 'add task cooking'...")
        chat_payload = {
            "message": "add task cooking",
            "conversation_id": None
        }
        
        chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
                                 headers=headers, 
                                 json=chat_payload)
        
        print(f"Response status: {chat_resp.status_code}")
        if chat_resp.status_code == 200:
            response_data = chat_resp.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
            
            # Check if it correctly recognized the add_task action
            response_text = response_data['response']
            if 'add_task' in response_text.lower() or 'cooking' in response_text.lower():
                print("✅ SUCCESS: The 'add task cooking' command was processed!")
            else:
                print("⚠️  The command was processed but may not have been recognized as an add_task action")
        else:
            print(f"Error response: {chat_resp.text}")
        
        # Test with "list tasks"
        print("\nTesting 'list tasks'...")
        chat_payload2 = {
            "message": "list tasks",
            "conversation_id": None  # Start a new conversation or use None
        }
        
        chat_resp2 = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
                                  headers=headers, 
                                  json=chat_payload2)
        
        print(f"Response status: {chat_resp2.status_code}")
        if chat_resp2.status_code == 200:
            response_data2 = chat_resp2.json()
            print(f"Response: {json.dumps(response_data2, indent=2)}")
        else:
            print(f"Error response: {chat_resp2.text}")
            
    else:
        print(f"Login failed: {login_resp.text}")
        
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()