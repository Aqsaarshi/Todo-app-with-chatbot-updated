import requests
import json
import os
from datetime import datetime

def test_hf_space_auth():
    """
    Test the Hugging Face Space deployment with proper authentication handling
    """
    print("Testing Hugging Face Space deployment...")
    print("="*60)
    
    BASE_URL = "https://aqsaarshi-todo-app-with-chatbot.hf.space"
    
    # Test 1: Health check
    print("1. Checking health endpoint...")
    try:
        health_resp = requests.get(f"{BASE_URL}/health")
        print(f"   Health status: {health_resp.status_code} - {health_resp.json()}")
    except Exception as e:
        print(f"   Health check failed: {e}")
        return
    
    # Test 2: Register a temporary user
    print("\n2. Registering a test user...")
    import uuid
    test_email = f"hf_test_{uuid.uuid4()}@example.com"
    register_data = {
        "email": test_email,
        "name": "HF Test User",
        "password": "securepassword123"
    }
    
    try:
        register_resp = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"   Registration status: {register_resp.status_code}")
        
        if register_resp.status_code == 200:
            register_json = register_resp.json()
            token = register_json.get('token')
            user_id = register_json.get('user_id')
            
            if token and user_id:
                print(f"   User registered successfully: {user_id}")
                
                # Test 3: Try chat endpoint with proper authentication
                print("\n3. Testing chat endpoint with authentication...")
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                chat_payload = {
                    "message": "create task hf space test",
                    "conversation_id": None
                }
                
                chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
                                         headers=headers, 
                                         json=chat_payload)
                
                print(f"   Chat response status: {chat_resp.status_code}")
                if chat_resp.status_code == 200:
                    print(f"   Chat response: {chat_resp.json()}")
                    print("\n   ✅ SUCCESS: Chatbot is working on Hugging Face Space!")
                else:
                    print(f"   Chat response: {chat_resp.text}")
                    print("\n   ❌ ISSUE: Chatbot not working on Hugging Face Space")
                    
                    # Additional debug info
                    print(f"   Token length: {len(token) if token else 'None'}")
                    print(f"   User ID: {user_id}")
                    print(f"   Headers sent: {list(headers.keys())}")
            else:
                print("   Failed to get token or user_id from registration")
                print(f"   Response: {register_json}")
        else:
            print(f"   Registration failed: {register_resp.text}")
            
    except Exception as e:
        print(f"   Error during testing: {e}")
        print("   This could be due to rate limiting or deployment issues on Hugging Face Space")


if __name__ == "__main__":
    test_hf_space_auth()