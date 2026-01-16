import asyncio
import requests
import json

async def test_chat_functionality():
    BASE_URL = "http://127.0.0.1:8001"

    # Login to get a valid token
    print("Logging in to get a valid token...")

    try:
        # First, login to get a token - login endpoint expects query parameters, not JSON
        login_resp = requests.post(f"{BASE_URL}/api/auth/login?email=testuser3@example.com&password=securepassword123")
        print(f"Login response: {login_resp.status_code}")
        
        if login_resp.status_code == 200:
            login_data = login_resp.json()
            print(f"Login success")
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
            response_data = chat_resp.json()
            print(f"Response: {response_data}")
            
            # Check if it correctly inferred the add_task action
            response_text = response_data['response']
            if 'add_task' in response_text.lower() or 'cooking' in response_text.lower():
                print("✅ SUCCESS: The 'add task cooking' command was correctly processed!")
            else:
                print("❌ ISSUE: The 'add task cooking' command was not processed correctly.")
                
            # Also test with a list command
            print(f"\nTesting chat endpoint with 'list tasks'...")
            chat_payload_list = {
                "message": "list tasks",
                "conversation_id": response_data['conversation_id']  # Use the conversation ID from the previous response
            }
            
            chat_resp_list = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
                                          headers=headers, 
                                          json=chat_payload_list)
            
            print(f"List response status: {chat_resp_list.status_code}")
            list_response_data = chat_resp_list.json()
            print(f"List Response: {list_response_data}")
            
            if 'list_tasks' in list_response_data['response'].lower():
                print("✅ SUCCESS: The 'list tasks' command was correctly processed!")
            else:
                print("❌ ISSUE: The 'list tasks' command was not processed correctly.")
                
        else:
            print(f"Login failed: {login_resp.text}")
            
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import subprocess
    import time
    import os
    
    # Skip starting the server since it's already running on port 8001
    print("Assuming server is running on port 8001...")
    
    # Wait for the server to start
    time.sleep(5)
    
    # Run the test
    import asyncio
    asyncio.run(test_chat_functionality())