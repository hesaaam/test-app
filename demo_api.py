#!/usr/bin/env python3
"""
Demo script showing additional API usage examples
"""

import requests
import json

# API base URL - using the public URL
BASE_URL = "http://62.60.198.230:5000/api"

def demo_validation_errors():
    """Demonstrate various validation errors"""
    print("🚨 Validation Error Examples")
    print("=" * 40)
    
    # Test 1: Invalid email format
    print("1. Invalid email format:")
    user_data = {
        "username": "testuser",
        "email": "not-an-email",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Error: {response.json().get('message', 'Unknown error')}")
    print()
    
    # Test 2: Username too short
    print("2. Username too short:")
    user_data = {
        "username": "ab",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Error: {response.json().get('message', 'Unknown error')}")
    print()
    
    # Test 3: Invalid age
    print("3. Invalid age:")
    user_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "age": 200
    }
    
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Error: {response.json().get('message', 'Unknown error')}")
    print()

def demo_successful_operations():
    """Demonstrate successful operations"""
    print("✅ Successful Operations Demo")
    print("=" * 40)
    
    # Create a new user
    user_data = {
        "username": "demo_user",
        "email": "demo.user@example.com",
        "first_name": "Demo",
        "last_name": "User",
        "age": 28
    }
    
    print("Creating a new user...")
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    result = response.json()
    
    if response.status_code == 201:
        user_id = result['user']['id']
        print(f"✅ User created with ID: {user_id}")
        print(f"Details: {json.dumps(result['user'], indent=2)}")
        print()
        
        # Update the user
        update_data = {
            "age": 29,
            "last_name": "UpdatedUser"
        }
        
        print("Updating user...")
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
        if response.status_code == 200:
            print("✅ User updated successfully")
            print(f"Updated details: {json.dumps(response.json()['user'], indent=2)}")
        print()
        
        # Get all users
        print("Getting all users...")
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            users = response.json()['users']
            print(f"✅ Total users: {len(users)}")
            for user in users:
                print(f"  - {user['username']} ({user['first_name']} {user['last_name']})")
        print()
        
        # Delete the user
        print("Deleting user...")
        response = requests.delete(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            print(f"✅ User {user_id} deleted successfully")
    else:
        print(f"❌ Failed to create user: {result.get('message', 'Unknown error')}")

def demo_error_handling():
    """Demonstrate error handling"""
    print("🛡️ Error Handling Demo")
    print("=" * 40)
    
    # Test non-existent user
    print("1. Getting non-existent user (ID: 9999):")
    response = requests.get(f"{BASE_URL}/users/9999")
    print(f"Status: {response.status_code}")
    print(f"Error: {response.json().get('message', 'Unknown error')}")
    print()
    
    # Test invalid user ID
    print("2. Getting user with invalid ID:")
    response = requests.get(f"{BASE_URL}/users/abc")
    print(f"Status: {response.status_code}")
    print(f"Error: {response.json().get('message', 'Unknown error')}")
    print()
    
    # Test missing required fields
    print("3. Creating user with missing fields:")
    user_data = {
        "username": "incomplete"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Error: {response.json().get('message', 'Unknown error')}")

def main():
    """Main demo function"""
    print("🌟 User Profile REST API Demo")
    print("=" * 50)
    print(f"API Base URL: {BASE_URL}")
    print()
    
    # Test health check
    print("🏥 Testing API Health...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ API is healthy and ready!")
        print(f"Response: {response.json()}")
    else:
        print("❌ API health check failed")
        return
    
    print("\n" + "=" * 50 + "\n")
    
    # Run demos
    try:
        demo_successful_operations()
        print("\n" + "=" * 50 + "\n")
        
        demo_error_handling()
        print("\n" + "=" * 50 + "\n")
        
        demo_validation_errors()
        
    except requests.exceptions.ConnectionError:
        print("❌ Unable to connect to the API server")
        print("Make sure the server is running on port 5000")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")

if __name__ == "__main__":
    main()