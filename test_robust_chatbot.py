import requests
import json
import time

print("Testing the robust chatbot task functionality...")

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
            "conversation_id": response_data.get('conversation_id')  # Use conversation ID from previous response
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

        # Test with "complete task 1" (assuming the task we added has ID 1)
        print("\nTesting 'complete task 1'...")
        chat_payload3 = {
            "message": "complete task 1",
            "conversation_id": response_data.get('conversation_id')
        }

        chat_resp3 = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                                  headers=headers,
                                  json=chat_payload3)

        print(f"Response status: {chat_resp3.status_code}")
        if chat_resp3.status_code == 200:
            response_data3 = chat_resp3.json()
            print(f"Response: {json.dumps(response_data3, indent=2)}")
        else:
            print(f"Error response: {chat_resp3.text}")

        # Test with "update task 1 to 'updated cooking'"
        print("\nTesting 'update task 1 to updated cooking'...")
        chat_payload4 = {
            "message": "update task 1 to updated cooking",
            "conversation_id": response_data.get('conversation_id')
        }

        chat_resp4 = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                                   headers=headers,
                                   json=chat_payload4)

        print(f"Response status: {chat_resp4.status_code}")
        if chat_resp4.status_code == 200:
            response_data4 = chat_resp4.json()
            print(f"Response: {json.dumps(response_data4, indent=2)}")
        else:
            print(f"Error response: {chat_resp4.text}")

        # Test with "delete task 1"
        print("\nTesting 'delete task 1'...")
        chat_payload5 = {
            "message": "delete task 1",
            "conversation_id": response_data.get('conversation_id')
        }

        chat_resp5 = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                                   headers=headers,
                                   json=chat_payload5)

        print(f"Response status: {chat_resp5.status_code}")
        if chat_resp5.status_code == 200:
            response_data5 = chat_resp5.json()
            print(f"Response: {json.dumps(response_data5, indent=2)}")
        else:
            print(f"Error response: {chat_resp5.text}")

        # Test with invalid commands to ensure error handling works
        print("\nTesting invalid command 'complete task invalid_id'...")
        chat_payload6 = {
            "message": "complete task invalid_id",
            "conversation_id": response_data.get('conversation_id')
        }

        chat_resp6 = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                                   headers=headers,
                                   json=chat_payload6)

        print(f"Response status: {chat_resp6.status_code}")
        if chat_resp6.status_code == 200:
            response_data6 = chat_resp6.json()
            print(f"Response: {json.dumps(response_data6, indent=2)}")
        else:
            print(f"Error response: {chat_resp6.text}")

        print("\n✅ All tests completed!")

    else:
        print(f"Login failed: {login_resp.text}")

except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()