import requests
import json
import re

# Test to debug the exact parsing issue
BASE_URL = "http://127.0.0.1:8000"

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
        
        # Test with a simple "add task" command to see what happens
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
        print(f"Full response: {json.dumps(response_data, indent=2)}")
        
        # Let's also try to manually test the parsing logic
        cohere_response = response_data['response']
        print(f"\nAnalyzing Cohere response: {cohere_response}")
        
        # Replicate the parsing logic from the backend
        if "ACTION:" in cohere_response:
            print("Found ACTION in response")
            # Extract everything after ACTION:
            action_match = cohere_response.split("ACTION:", 1)
            if len(action_match) > 1:
                remaining_text = action_match[1].strip()
                print(f"Text after ACTION: {remaining_text}")

                # Extract action line (first non-empty line that doesn't start with {)
                lines = remaining_text.split('\n')
                print(f"All lines: {lines}")
                
                for i, line in enumerate(lines):
                    stripped_line = line.strip()
                    print(f"Processing line {i}: '{stripped_line}'")
                    if stripped_line and not stripped_line.startswith('{'):
                        # This line contains the action
                        # Extract just the action word (first word before any space or colon)
                        action_words = stripped_line.split()
                        print(f"Action words: {action_words}")
                        if action_words:
                            action = action_words[0].rstrip(':')  # Remove trailing colon if present
                            print(f"Extracted action: {action}")
                        
                        # Look for the next line that starts with { which should be parameters
                        for j in range(i+1, len(lines)):
                            next_line = lines[j].strip()
                            print(f"Checking next line {j}: '{next_line}'")
                            if next_line.startswith('{'):
                                print(f"Found JSON parameters: {next_line}")
                        break
        else:
            print("No ACTION found in response")
        
    else:
        print(f"Login failed: {login_resp.text}")
        
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()