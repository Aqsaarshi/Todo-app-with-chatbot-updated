import requests
import json

# Base URL for the backend
BASE_URL = "http://127.0.0.1:8001"

def login_user():
    url = f"{BASE_URL}/api/auth/login"

    # Login with the original credentials that were failing
    params = {
        "email": "aqsaarshi5@gmail.com",
        "password": "aqsa123"
    }

    try:
        # The login endpoint expects query parameters
        response = requests.post(url, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("Login successful!")
            return response.json()
        else:
            print(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None

if __name__ == "__main__":
    print("Attempting to login user...")
    result = login_user()
    if result:
        print(f"Login result: {result}")