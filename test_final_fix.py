import requests
import json

# Test if the chatbot now properly recognizes "add task" commands
BASE_URL = "http://127.0.0.1:8000"

# Login to get a valid token
print("Logging in to get a valid token...")

try:
    # First, login to get a token - login endpoint expects query parameters, not JSON
    login_resp = requests.post(f"{BASE_URL}/api/auth/login?email=testuser3@example.com&password=securepassword123")
    print(f"Login response: {login_resp.status_code}")
    
    if login_resp.status_code == 200:
        login_data = login_resp.json()
        print(f"Login successful")
        token = login_data['token']
        user_id = login_data['user_id']
        print(f"User ID: {user_id}")
        
        # Test with "add task cooking" command
        print(f"\nTesting chat endpoint with 'add task cooking'...")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        chat_payload = {
            "message": "add task cooking",
            "conversation_id": None
        }
        
        # Try the chat endpoint
        chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
                                 headers=headers, 
                                 json=chat_payload)
        
        print(f"Chat response status: {chat_resp.status_code}")
        if chat_resp.status_code == 200:
            response_data = chat_resp.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
            
            # Check if it correctly recognized the add_task action
            response_text = response_data['response']
            if 'add_task' in response_text.lower():
                print("✅ SUCCESS: The 'add task cooking' command was correctly processed!")
                if 'cooking' in response_text.lower():
                    print("✅ SUCCESS: The task title 'cooking' was correctly extracted!")
            else:
                print("❌ The 'add task cooking' command was not processed as expected.")
                
            # Also test with "add task aqsa" command
            print(f"\nTesting chat endpoint with 'add task aqsa'...")
            chat_payload2 = {
                "message": "add task aqsa",
                "conversation_id": response_data['conversation_id']  # Use the conversation ID from the previous response
            }
            
            chat_resp2 = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
                                      headers=headers, 
                                      json=chat_payload2)
            
            print(f"Chat response status: {chat_resp2.status_code}")
            if chat_resp2.status_code == 200:
                response_data2 = chat_resp2.json()
                print(f"Response: {json.dumps(response_data2, indent=2)}")
                
                response_text2 = response_data2['response']
                if 'add_task' in response_text2.lower():
                    print("✅ SUCCESS: The 'add task aqsa' command was correctly processed!")
                    if 'aqsa' in response_text2.lower():
                        print("✅ SUCCESS: The task title 'aqsa' was correctly extracted!")
                else:
                    print("❌ The 'add task aqsa' command was not processed as expected.")
        else:
            print(f"Chat request failed with status: {chat_resp.status_code}")
            print(f"Response text: {chat_resp.text}")
        
    else:
        print(f"Login failed: {login_resp.text}")
        
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()