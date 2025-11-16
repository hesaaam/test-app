#!/bin/bash

# User Profile REST API Demo using curl
# This script demonstrates various API endpoints using curl commands

echo "🌟 User Profile REST API Demo with cURL"
echo "====================================="
echo "API Base URL: http://62.60.198.230:5000/api"
echo ""

# Function to print colored output
print_success() {
    echo -e "\033[32m✅ $1\033[0m"
}

print_error() {
    echo -e "\033[31m❌ $1\033[0m"
}

print_info() {
    echo -e "\033[34mℹ️  $1\033[0m"
}

# Health Check
echo "🏥 Health Check:"
echo "curl -X GET http://62.60.198.230:5000/api/health"
curl -s -X GET "http://62.60.198.230:5000/api/health" | python3 -m json.tool
echo ""

# Get All Users
echo "👥 Get All Users:"
echo "curl -X GET http://62.60.198.230:5000/api/users"
curl -s -X GET "http://62.60.198.230:5000/api/users" | python3 -m json.tool
echo ""

# Get Specific User (valid)
echo "👤 Get User ID 1 (valid):"
echo "curl -X GET http://62.60.198.230:5000/api/users/1"
curl -s -X GET "http://62.60.198.230:5000/api/users/1" | python3 -m json.tool
echo ""

# Get Specific User (invalid ID)
echo "❌ Get User ID 'invalid' (validation error):"
echo "curl -X GET http://62.60.198.230:5000/api/users/invalid"
curl -s -X GET "http://62.60.198.230:5000/api/users/invalid" | python3 -m json.tool
echo ""

# Get Non-existent User
echo "❌ Get User ID 9999 (not found):"
echo "curl -X GET http://62.60.198.230:5000/api/users/9999"
curl -s -X GET "http://62.60.198.230:5000/api/users/9999" | python3 -m json.tool
echo ""

# Create User (successful)
echo "➕ Create User (successful):"
echo 'curl -X POST http://62.60.198.230:5000/api/users \
  -H "Content-Type: application/json" \
  -d '''{
    "username": "demo_curl",
    "email": "demo.curl@example.com",
    "first_name": "Demo",
    "last_name": "Curl",
    "age": 30
  }'\'''
curl -s -X POST "http://62.60.198.230:5000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_curl",
    "email": "demo.curl@example.com",
    "first_name": "Demo",
    "last_name": "Curl",
    "age": 30
  }' | python3 -m json.tool
echo ""

# Create User (validation error - missing fields)
echo "❌ Create User (missing required fields):"
echo 'curl -X POST http://62.60.198.230:5000/api/users \
  -H "Content-Type: application/json" \
  -d '''{"username": "incomplete"}'\'''
curl -s -X POST "http://62.60.198.230:5000/api/users" \
  -H "Content-Type: application/json" \
  -d '{"username": "incomplete"}' | python3 -m json.tool
echo ""

# Create User (validation error - invalid email)
echo "❌ Create User (invalid email):"
echo 'curl -X POST http://62.60.198.230:5000/api/users \
  -H "Content-Type: application/json" \
  -d '''{
    "username": "test_email",
    "email": "not-an-email",
    "first_name": "Test",
    "last_name": "Email"
  }'\'''
curl -s -X POST "http://62.60.198.230:5000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_email",
    "email": "not-an-email",
    "first_name": "Test",
    "last_name": "Email"
  }' | python3 -m json.tool
echo ""

# Update User (successful)
echo "✏️  Update User ID 1:"
echo 'curl -X PUT http://62.60.198.230:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '''{"age": 31}'\'''
curl -s -X PUT "http://62.60.198.230:5000/api/users/1" \
  -H "Content-Type: application/json" \
  -d '{"age": 31}' | python3 -m json.tool
echo ""

echo "🎉 cURL Demo completed!"
echo ""
echo "Note: The API server is running with sample data. In a production"
echo "environment, you would connect this to a real database and add"
echo "authentication, rate limiting, and other security measures."