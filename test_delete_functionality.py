#!/usr/bin/env python3
"""
Test script to verify the delete functionality works with the backend API
"""
import asyncio
import aiohttp
import uuid
from datetime import datetime

async def test_delete_functionality():
    # Backend URL
    base_url = "https://aqsaarshi-todo-app-backend.hf.space"

    # Test user credentials
    test_user = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }

    async with aiohttp.ClientSession() as session:
        print("Testing delete functionality...")

        # Try to register a test user (ignore errors if user already exists)
        try:
            register_resp = await session.post(
                f"{base_url}/api/auth/register",
                json=test_user
            )
            print(f"Registration status: {register_resp.status}")
            if register_resp.status == 200:
                register_data = await register_resp.json()
                token = register_data.get('token')
                user_id = register_data.get('user_id')
                print(f"Registered user: {user_id}")
            else:
                # If registration failed, try to login
                login_resp = await session.post(
                    f"{base_url}/api/auth/login",
                    params={"email": test_user['email'], "password": test_user['password']}
                )
                print(f"Login status: {login_resp.status}")
                if login_resp.status == 200:
                    login_data = await login_resp.json()
                    token = login_data.get('token')
                    user_id = login_data.get('user_id')
                    print(f"Logged in user: {user_id}")
                else:
                    print("Could not register or login user")
                    return
        except Exception as e:
            print(f"Error registering/logging in: {e}")
            return

        # Create a test task
        try:
            create_task_resp = await session.post(
                f"{base_url}/api/{user_id}/tasks?token={token}",
                json={
                    "title": "Test task for deletion",
                    "description": "This is a test task that will be deleted",
                    "priority": "medium"
                }
            )
            print(f"Create task status: {create_task_resp.status}")
            if create_task_resp.status == 200:
                task_data = await create_task_resp.json()
                task_id = task_data.get('id')
                print(f"Created task: {task_id}")

                # Now try to delete the task
                delete_resp = await session.delete(
                    f"{base_url}/api/{user_id}/tasks/{task_id}?token={token}"
                )
                print(f"Delete task status: {delete_resp.status}")
                if delete_resp.status == 200:
                    print("Successfully deleted task!")
                    response_data = await delete_resp.json()
                    print(f"Response: {response_data}")
                else:
                    print(f"Failed to delete task: {delete_resp.status}")
                    error_text = await delete_resp.text()
                    print(f"Error: {error_text}")
            else:
                print("Failed to create test task")
                error_text = await create_task_resp.text()
                print(f"Error: {error_text}")
        except Exception as e:
            print(f"Error during task creation/deletion: {e}")

if __name__ == "__main__":
    asyncio.run(test_delete_functionality())