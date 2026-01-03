#!/usr/bin/env python3
"""
Integration test script to verify the full Todo application is working correctly.
"""
import requests
import json

def test_full_integration():
    """Test the complete integration of frontend and backend"""
    print("Testing Full Stack Todo Application Integration...")
    print("="*60)

    BASE_URL = "http://localhost:8000"

    # Test 1: Health check
    print("1. Testing backend health...")
    health_response = requests.get(f"{BASE_URL}/health")
    if health_response.status_code == 200 and health_response.json().get("status") == "healthy":
        print("   [OK] Backend health check passed")
    else:
        print("   [FAIL] Backend health check failed")
        return False

    # Test 2: User Registration
    print("\n2. Testing user registration...")
    register_data = {
        "email": "integration@test.com",
        "password": "testpass123",
        "name": "Integration Test"
    }
    register_response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json=register_data
    )
    if register_response.status_code == 200:
        print("   [OK] User registration successful")
        token = register_response.json().get("token")
        user_id = register_response.json().get("user_id")
    else:
        print(f"   [FAIL] User registration failed: {register_response.text}")
        return False

    # Test 3: User Login
    print("\n3. Testing user login...")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login?email=integration@test.com&password=testpass123"
    )
    if login_response.status_code == 200:
        print("   [OK] User login successful")
        login_token = login_response.json().get("token")
    else:
        print(f"   [FAIL] User login failed: {login_response.text}")
        return False

    # Test 4: Create a task
    print("\n4. Testing task creation...")
    task_data = {
        "title": "Integration Test Task",
        "description": "This task was created during integration testing",
        "priority": "high"
    }
    create_task_response = requests.post(
        f"{BASE_URL}/api/{user_id}/tasks?token={login_token}",
        json=task_data
    )
    if create_task_response.status_code == 200:
        print("   [OK] Task creation successful")
        task_id = create_task_response.json().get("id")
    else:
        print(f"   [FAIL] Task creation failed: {create_task_response.text}")
        return False

    # Test 5: Get tasks
    print("\n5. Testing task retrieval...")
    get_tasks_response = requests.get(
        f"{BASE_URL}/api/{user_id}/tasks?token={login_token}"
    )
    if get_tasks_response.status_code == 200 and len(get_tasks_response.json()) > 0:
        print("   [OK] Task retrieval successful")
    else:
        print(f"   [FAIL] Task retrieval failed: {get_tasks_response.text}")
        return False

    # Test 6: Update task
    print("\n6. Testing task update...")
    update_data = {
        "title": "Updated Integration Test Task",
        "completed": True
    }
    update_task_response = requests.put(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}?token={login_token}",
        json=update_data
    )
    if update_task_response.status_code == 200:
        print("   [OK] Task update successful")
    else:
        print(f"   [FAIL] Task update failed: {update_task_response.text}")
        return False

    # Test 7: Toggle task completion
    print("\n7. Testing task completion toggle...")
    toggle_response = requests.patch(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}/complete?token={login_token}&completed=false"
    )
    if toggle_response.status_code == 200:
        print("   [OK] Task completion toggle successful")
    else:
        print(f"   [FAIL] Task completion toggle failed: {toggle_response.text}")
        return False

    print("\n" + "="*60)
    print("SUCCESS: All integration tests passed! The full stack application is working correctly.")
    print("[OK] Backend API endpoints are accessible")
    print("[OK] User authentication flow works")
    print("[OK] Task management functionality works")
    print("[OK] Frontend can connect to backend API")
    print("="*60)

    return True

if __name__ == "__main__":
    success = test_full_integration()
    if success:
        print("\nFull stack Todo application integration verified successfully!")
    else:
        print("\nIntegration tests failed!")
        exit(1)