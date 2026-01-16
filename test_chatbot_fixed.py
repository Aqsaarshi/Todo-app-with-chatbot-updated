#!/usr/bin/env python3
"""
Test script to verify the chatbot functionality is working properly after fixes.
"""
import requests
import json
import uuid
from datetime import datetime

def test_chatbot_functionality():
    """Test the chatbot functionality directly"""
    print("Testing Chatbot Functionality After Fixes...")
    print("="*60)

    # Using a local backend server - adjust the URL if your server is running elsewhere
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # Since we need a valid user ID and token for the chat endpoint, 
    # we'll need to register a test user first
    
    # Step 1: Register a test user
    print("1. Registering test user...")
    user_email = f"test_{uuid.uuid4()}@example.com"
    user_data = {
        "email": user_email,
        "password": "testpass123",
        "name": "Test User"
    }
    
    try:
        register_response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if register_response.status_code == 200:
            print("   [OK] Test user registered successfully")
            token = register_response.json().get("token")
            user_id = register_response.json().get("user_id")
        else:
            print(f"   [FAIL] User registration failed: {register_response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Could not connect to backend: {e}")
        print("   Make sure your backend server is running on http://127.0.0.1:8000")
        return False

    # Step 2: Test chatbot with a task creation command
    print("\n2. Testing chatbot with 'create task driving' command...")
    chat_payload = {
        "message": "create task driving",
        "conversation_id": None
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        chat_response = requests.post(f"{BASE_URL}/{user_id}/chat", json=chat_payload, headers=headers)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"   [OK] Chat response received")
            print(f"   Response: {response_data.get('response', 'No response text')}")
            
            # Check if any tool calls were made
            tool_calls = response_data.get('tool_calls', [])
            if tool_calls:
                print(f"   Tool calls executed: {len(tool_calls)}")
                for call in tool_calls:
                    print(f"     - {call.get('tool_name', 'Unknown')} tool")
                    print(f"       Result: {call.get('result', {})}")
                print("   [SUCCESS] Task creation command was properly recognized and executed!")
            else:
                print("   [ISSUE] No tool calls were executed (the AI didn't recognize the command)")
                
            conversation_id = response_data.get('conversation_id')
        else:
            print(f"   [FAIL] Chat request failed: {chat_response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Chat request failed: {e}")
        return False

    # Step 3: Test chatbot with a task listing command
    print("\n3. Testing chatbot with 'list tasks' command...")
    chat_payload = {
        "message": "list tasks",
        "conversation_id": conversation_id
    }
    
    try:
        chat_response = requests.post(f"{BASE_URL}/{user_id}/chat", json=chat_payload, headers=headers)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"   [OK] Chat response received")
            print(f"   Response: {response_data.get('response', 'No response text')}")
            
            # Check if any tool calls were made
            tool_calls = response_data.get('tool_calls', [])
            if tool_calls:
                print(f"   Tool calls executed: {len(tool_calls)}")
                for call in tool_calls:
                    print(f"     - {call.get('tool_name', 'Unknown')} tool")
            else:
                print("   No tool calls were executed")
        else:
            print(f"   [FAIL] Chat request failed: {chat_response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Chat request failed: {e}")
        return False

    print("\n" + "="*60)
    print("Chatbot functionality test completed.")
    print("Check if the AI properly recognized and executed commands.")
    print("="*60)

    return True

if __name__ == "__main__":
    test_chatbot_functionality()