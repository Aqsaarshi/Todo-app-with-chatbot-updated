import requests
import json

# Simple test to check if the server is working at all
BASE_URL = "http://127.0.0.1:8000"

# Test the root endpoint first
print("Testing root endpoint...")
try:
    root_resp = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint response: {root_resp.status_code}")
    print(f"Root endpoint data: {root_resp.text}")
except Exception as e:
    print(f"Error testing root endpoint: {e}")

# Test the health endpoint
print("\nTesting health endpoint...")
try:
    health_resp = requests.get(f"{BASE_URL}/health")
    print(f"Health endpoint response: {health_resp.status_code}")
    print(f"Health endpoint data: {health_resp.text}")
except Exception as e:
    print(f"Error testing health endpoint: {e}")

# Test auth endpoint
print("\nTesting auth endpoint...")
try:
    auth_resp = requests.get(f"{BASE_URL}/api/auth")
    print(f"Auth endpoint response: {auth_resp.status_code}")
    print(f"Auth endpoint data: {auth_resp.text}")
except Exception as e:
    print(f"Error testing auth endpoint: {e}")