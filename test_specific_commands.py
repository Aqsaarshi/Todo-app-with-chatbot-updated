import requests
import json

# Test the chat endpoint with specific commands that should be recognized
BASE_URL = "http://127.0.0.1:8000"

# Use the same user from the previous test
user_id = "839585cd-7451-49af-a8b9-71d4dbf7f6d1"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4Mzk1ODVjZC03NDUxLTQ5YWYtYThiOS03MWQ0ZGJmN2Y2ZDEiLCJlbWFpbCI6InRlc3R1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzY4NTgzMjczfQ.r-a3wei3HU_QTABTj_UCBYF0FPmXiB3dKg731kwoyw8"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Get the conversation ID from the previous test where we added tasks
conversation_id = 53  # From the previous test

# Test 1: List tasks using the specific command
print("Test 1: Listing tasks with specific command...")
chat_payload = {
    "message": "list tasks",
    "conversation_id": conversation_id
}

chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                         headers=headers,
                         json=chat_payload)

print(f"Response: {chat_resp.json()}")

print("\n" + "="*50 + "\n")

# Test 2: Complete a task using the specific command
print("Test 2: Completing a task with specific command...")
chat_payload = {
    "message": "complete task 974ad034-aa10-437d-821a-f8424475ef93",  # UUID of 'buy groceries' task
    "conversation_id": conversation_id
}

chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                         headers=headers,
                         json=chat_payload)

print(f"Response: {chat_resp.json()}")

print("\n" + "="*50 + "\n")

# Test 3: Try to list tasks again to see if the completed task shows as completed
print("Test 3: Listing tasks again to see completion status...")
chat_payload = {
    "message": "list tasks",
    "conversation_id": conversation_id
}

chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat",
                         headers=headers,
                         json=chat_payload)

print(f"Response: {chat_resp.json()}")