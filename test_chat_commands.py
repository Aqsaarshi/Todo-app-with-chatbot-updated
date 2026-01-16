import requests
import json

# Test the chat endpoint with various commands
BASE_URL = "http://127.0.0.1:8000"

# Use the same user from the previous test
user_id = "839585cd-7451-49af-a8b9-71d4dbf7f6d1"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4Mzk1ODVjZC03NDUxLTQ5YWYtYThiOS03MWQ0ZGJmN2Y2ZDEiLCJlbWFpbCI6InRlc3R1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzY4NTgzMjczfQ.r-a3wei3HU_QTABTj_UCBYF0FPmXiB3dKg731kwoyw8"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Test 1: Add another task
print("Test 1: Adding another task...")
chat_payload = {
    "message": "Add task buy groceries",
    "conversation_id": None  # Start a new conversation
}

chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                         headers=headers,
                         json=chat_payload)

print(f"Response: {chat_resp.json()}")
conversation_id = chat_resp.json()['conversation_id']

print("\n" + "="*50 + "\n")

# Test 2: List tasks in the same conversation
print("Test 2: Listing tasks...")
chat_payload = {
    "message": "What tasks do I have?",
    "conversation_id": conversation_id  # Continue the conversation
}

chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                         headers=headers,
                         json=chat_payload)

print(f"Response: {chat_resp.json()}")

print("\n" + "="*50 + "\n")

# Test 3: Complete a task
print("Test 3: Completing a task...")
chat_payload = {
    "message": "Complete the 'buy groceries' task",
    "conversation_id": conversation_id
}

chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                         headers=headers,
                         json=chat_payload)

print(f"Response: {chat_resp.json()}")

print("\n" + "="*50 + "\n")

# Test 4: Add another task using different phrasing
print("Test 4: Adding task with different phrasing...")
chat_payload = {
    "message": "Create a new task to call mom",
    "conversation_id": conversation_id
}

chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                         headers=headers,
                         json=chat_payload)

print(f"Response: {chat_resp.json()}")