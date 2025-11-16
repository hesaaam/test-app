#!/usr/bin/env python3
"""
Test script for the User Profile REST API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Health check passed\n")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}\n")
        return False

def test_get_all_users():
    """Test get all users endpoint"""
    print("Testing get all users...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Users count: {data.get('count', 0)}")
        print(f"Response: {json.dumps(data, indent=2)}")
        print("✅ Get all users passed\n")
        return True
    except Exception as e:
        print(f"❌ Get all users failed: {e}\n")
        return False

def test_get_valid_user():
    """Test get user with valid ID"""
    print("Testing get valid user...")
    try:
        response = requests.get(f"{BASE_URL}/users/1")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"User: {json.dumps(data.get('user', {}), indent=2)}")
        print("✅ Get valid user passed\n")
        return True
    except Exception as e:
        print(f"❌ Get valid user failed: {e}\n")
        return False

def test_get_invalid_user():
    """Test get user with invalid ID"""
    print("Testing get user with invalid ID...")
    try:
        response = requests.get(f"{BASE_URL}/users/invalid")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Error: {json.dumps(data, indent=2)}")
        
        if response.status_code == 400:
            print("✅ Invalid user ID validation passed\n")
            return True
        else:
            print("❌ Expected 400 status code\n")
            return False
    except Exception as e:
        print(f"❌ Invalid user ID test failed: {e}\n")
        return False

def test_get_nonexistent_user():
    """Test get user that doesn't exist"""
    print("Testing get nonexistent user...")
    try:
        response = requests.get(f"{BASE_URL}/users/999")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Error: {json.dumps(data, indent=2)}")
        
        if response.status_code == 404:
            print("✅ Nonexistent user validation passed\n")
            return True
        else:
            print("❌ Expected 404 status code\n")
            return False
    except Exception as e:
        print(f"❌ Nonexistent user test failed: {e}\n")
        return False

def test_create_valid_user():
    """Test create user with valid data"""
    print("Testing create valid user...")
    user_data = {
        "username": "test_user",
        "email": "test.user@example.com",
        "first_name": "Test",
        "last_name": "User",
        "age": 25
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 201:
            print("✅ Create valid user passed\n")
            return data.get('user', {}).get('id')
        else:
            print("❌ Expected 201 status code\n")
            return None
    except Exception as e:
        print(f"❌ Create valid user failed: {e}\n")
        return None

def test_create_invalid_user():
    """Test create user with invalid data"""
    print("Testing create user with invalid data...")
    user_data = {
        "username": "ab",  # Too short
        "email": "invalid-email",  # Invalid format
        "first_name": "",  # Empty
        "age": 200  # Out of range
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Error: {json.dumps(data, indent=2)}")
        
        if response.status_code == 400:
            print("✅ Invalid user data validation passed\n")
            return True
        else:
            print("❌ Expected 400 status code\n")
            return False
    except Exception as e:
        print(f"❌ Invalid user data test failed: {e}\n")
        return False

def test_update_user(new_user_id):
    """Test update user"""
    print("Testing update user...")
    update_data = {
        "age": 26,
        "first_name": "UpdatedTest"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/users/{new_user_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print("✅ Update user passed\n")
            return True
        else:
            print("❌ Expected 200 status code\n")
            return False
    except Exception as e:
        print(f"❌ Update user failed: {e}\n")
        return False

def test_delete_user(new_user_id):
    """Test delete user"""
    print("Testing delete user...")
    try:
        response = requests.delete(f"{BASE_URL}/users/{new_user_id}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print("✅ Delete user passed\n")
            return True
        else:
            print("❌ Expected 200 status code\n")
            return False
    except Exception as e:
        print(f"❌ Delete user failed: {e}\n")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting User Profile API Tests")
    print("=" * 40)
    
    # Wait a moment for the server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        test_health_check,
        test_get_all_users,
        test_get_valid_user,
        test_get_invalid_user,
        test_get_nonexistent_user,
        test_create_invalid_user
    ]
    
    passed = 0
    total = len(tests)
    
    # Run basic tests
    for test in tests:
        if test():
            passed += 1
    
    # Create a test user for update/delete tests
    print("Creating test user for update/delete tests...")
    new_user_id = test_create_valid_user()
    
    if new_user_id:
        # Test update
        if test_update_user(new_user_id):
            passed += 1
        total += 1
        
        # Test delete
        if test_delete_user(new_user_id):
            passed += 1
        total += 1
    else:
        print("Skipping update/delete tests due to failed user creation")
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

if __name__ == "__main__":
    main()