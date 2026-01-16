import requests
import uuid
import time
import sys

# Wait a moment for the server to be ready
time.sleep(2)

# Test registering a user
base_url = 'http://127.0.0.1:8000/api'
user_email = f'test_{uuid.uuid4()}@example.com'
user_data = {
    'email': user_email,
    'password': 'testpass123',
    'name': 'Test User'
}

try:
    print('Testing user registration...')
    register_response = requests.post(f'{base_url}/auth/register', json=user_data)
    print(f'Register response status: {register_response.status_code}')
    
    if register_response.status_code == 200:
        response_json = register_response.json()
        token = response_json.get('token')
        user_id = response_json.get('user_id')
        print(f'[OK] User registered successfully. User ID: {user_id}')

        # Now test the chat endpoint
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        chat_payload = {
            'message': 'create task test task from simple test',
            'conversation_id': None
        }

        print('Testing chat endpoint...')
        chat_response = requests.post(f'{base_url}/{user_id}/chat', json=chat_payload, headers=headers)
        print(f'Chat response status: {chat_response.status_code}')
        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            print(f'[OK] Chat response: {chat_data["response"]}')
            print('[OK] SUCCESS: Chatbot is working!')
        else:
            print(f'[ERROR] Chat error: {chat_response.text}')
    else:
        print(f'[ERROR] Registration failed: {register_response.text}')

except Exception as e:
    print(f'[ERROR] Error during test: {e}')
    import traceback
    traceback.print_exc()