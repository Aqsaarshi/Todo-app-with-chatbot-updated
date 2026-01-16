#!/usr/bin/env python3
"""
Debug script to test API endpoints and understand the expected request formats
"""

import requests
import json
import uuid

# Base URL for the backend
BASE_URL = "http://localhost:8000"  # Adjust this to your backend URL

def test_conversations_endpoint(user_id, token):
    """
    Test the conversations endpoint with proper parameters
    """
    print(f"Testing conversations endpoint for user: {user_id}")
    
    url = f"{BASE_URL}/{user_id}/conversations"
    
    # Headers with the token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Parameters
    params = {
        "limit": 10,
        "offset": 0
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("SUCCESS: Retrieved conversations")
        else:
            print(f"ERROR: Failed to retrieve conversations - {response.status_code}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_chat_endpoint(user_id, token):
    """
    Test the chat endpoint with proper request format
    """
    print(f"\nTesting chat endpoint for user: {user_id}")
    
    url = f"{BASE_URL}/{user_id}/chat"
    
    # Headers with the token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Proper request body format
    data = {
        "message": "Add task driving",
        "conversation_id": None  # Will create a new conversation
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("SUCCESS: Chat message processed")
        else:
            print(f"ERROR: Failed to process chat - {response.status_code}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")

def show_correct_usage():
    """
    Show the correct way to call the API endpoints
    """
    print("\nCORRECT USAGE OF THE API ENDPOINTS:")
    print("="*50)
    
    print("\n1. GET /{user_id}/conversations")
    print("   Headers Required:")
    print("   - Authorization: Bearer {token}")
    print("   Query Parameters:")
    print("   - limit: number of conversations to return (optional, default 10)")
    print("   - offset: number of conversations to skip (optional, default 0)")
    print("   \n   Example:")
    print("   GET /dc9f498e-b24f-43d3-aff5-4398d90a4140/conversations")
    print("   Headers: {\"Authorization\": \"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...\"}")
    
    print("\n2. POST /{user_id}/chat")
    print("   Headers Required:")
    print("   - Authorization: Bearer {token}")
    print("   - Content-Type: application/json")
    print("   \n   Request Body:")
    print("   {")
    print('     "message": "your message here",')
    print("     \"conversation_id\": \"existing_conversation_id or null\"")
    print("   }")
    print("   \n   Example:")
    print("   POST /dc9f498e-b24f-43d3-aff5-4398d90a4140/chat")
    print("   Headers: {\"Authorization\": \"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...\", \"Content-Type\": \"application/json\"}")
    print("   Body: {\"message\": \"Add task driving\", \"conversation_id\": null}")

if __name__ == "__main__":
    print("API Endpoint Debug Script")
    print("="*50)
    
    show_correct_usage()
    
    print("\n" + "="*50)
    print("To get a valid token, you need to:")
    print("1. Register a user: POST /auth/register")
    print("2. Login: POST /auth/login") 
    print("3. Use the returned token in subsequent requests")
    
    # Note: Uncomment the following lines with valid user_id and token to test
    # sample_user_id = "dc9f498e-b24f-43d3-aff5-4398d90a4140"  # Use a valid UUID from your DB
    # sample_token = "YOUR_VALID_JWT_TOKEN_HERE"  # You need to get this from login
    # test_conversations_endpoint(sample_user_id, sample_token)
    # test_chat_endpoint(sample_user_id, sample_token)