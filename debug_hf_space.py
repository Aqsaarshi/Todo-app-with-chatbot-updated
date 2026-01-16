import requests
import json

def debug_hf_space():
    """
    Debug the Hugging Face Space authentication issue
    """
    print("Debugging Hugging Face Space authentication...")
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
    test_email = f"debug_{uuid.uuid4()}@example.com"
    register_data = {
        "email": test_email,
        "name": "Debug User",
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
                print(f"   Token received (length: {len(token)})")
                
                # Test 3: Try to decode the token to see its structure
                print("\n3. Analyzing token structure...")
                import base64
                try:
                    # Split the token to get the payload part
                    parts = token.split('.')
                    if len(parts) == 3:
                        # Decode the payload (second part)
                        payload = parts[1]
                        # Add padding if needed
                        payload += '=' * (4 - len(payload) % 4)
                        decoded_payload = base64.b64decode(payload)
                        import json
                        payload_json = json.loads(decoded_payload)
                        print(f"   Token payload: {payload_json}")
                        
                        # Extract user ID from token
                        token_user_id = payload_json.get('sub')
                        print(f"   User ID in token: {token_user_id}")
                        print(f"   Path user ID: {user_id}")
                        print(f"   Match: {token_user_id == user_id}")
                        
                    else:
                        print("   Unexpected token format")
                except Exception as e:
                    print(f"   Could not decode token: {e}")
                
                # Test 4: Try chat endpoint with proper authentication
                print("\n4. Testing chat endpoint with authentication...")
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                print(f"   Headers being sent: {headers.keys()}")
                
                chat_payload = {
                    "message": "create task debug test",
                    "conversation_id": None
                }
                
                print(f"   Making request to: {BASE_URL}/api/{user_id}/chat")
                
                chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
                                         headers=headers, 
                                         json=chat_payload)
                
                print(f"   Chat response status: {chat_resp.status_code}")
                print(f"   Chat response: {chat_resp.text}")
                
                if chat_resp.status_code == 200:
                    print("\n   [SUCCESS]: Chatbot is working on Hugging Face Space!")
                else:
                    print("\n   [ISSUE]: Chatbot not working on Hugging Face Space")
                    print("   Possible causes:")
                    print("   - Different SECRET_KEY in Hugging Face environment")
                    print("   - Different ALGORITHM in Hugging Face environment")
                    print("   - Token expiration or validation issues")
                    print("   - Rate limiting")
            else:
                print("   Failed to get token or user_id from registration")
                print(f"   Response: {register_json}")
        else:
            print(f"   Registration failed: {register_resp.text}")
            
    except Exception as e:
        print(f"   Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    debug_hf_space()