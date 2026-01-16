import requests
import json

# Base URL for the backend
BASE_URL = "http://127.0.0.1:8001"

# Register a new user
def register_user():
    url = f"{BASE_URL}/api/auth/register"
    
    user_data = {
        "email": "aqsaarshi5@gmail.com",
        "name": "Aqsa Arshi",
        "password": "aqsa123"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, data=json.dumps(user_data), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("User registered successfully!")
            return response.json()
        else:
            print(f"Failed to register user: {response.text}")
            return None
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None

if __name__ == "__main__":
    print("Attempting to register user...")
    result = register_user()
    if result:
        print(f"Registration result: {result}")