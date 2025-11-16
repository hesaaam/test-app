#!/usr/bin/env python3
"""
Simple REST API for user profile information with proper error handling and input validation.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Sample user data (in a real app, this would come from a database)
USERS_DB = {
    1: {
        "id": 1,
        "username": "john_doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "created_at": "2023-01-15T10:30:00Z"
    },
    2: {
        "id": 2,
        "username": "jane_smith",
        "email": "jane.smith@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "age": 28,
        "created_at": "2023-02-20T14:45:00Z"
    },
    3: {
        "id": 3,
        "username": "bob_johnson",
        "email": "bob.johnson@example.com",
        "first_name": "Bob",
        "last_name": "Johnson",
        "age": 35,
        "created_at": "2023-03-10T09:15:00Z"
    }
}

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_user_id(user_id):
    """Validate user ID"""
    if not isinstance(user_id, int):
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            raise ValidationError("User ID must be a valid integer")
    
    if user_id <= 0:
        raise ValidationError("User ID must be a positive integer")
    
    return user_id

def validate_email(email):
    """Validate email format"""
    if not email:
        raise ValidationError("Email is required")
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError("Invalid email format")
    
    return email

def validate_username(username):
    """Validate username"""
    if not username:
        raise ValidationError("Username is required")
    
    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long")
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError("Username can only contain letters, numbers, and underscores")
    
    return username

def validate_age(age):
    """Validate age"""
    if age is not None:
        try:
            age = int(age)
            if age < 0 or age > 150:
                raise ValidationError("Age must be between 0 and 150")
            return age
        except (ValueError, TypeError):
            raise ValidationError("Age must be a valid number")
    return age

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Resource not found",
        "message": "The requested resource could not be found",
        "status_code": 404,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        "error": "Bad request",
        "message": str(error.description) if hasattr(error, 'description') else "Invalid request data",
        "status_code": 400,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 400

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred",
        "status_code": 500,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 500

@app.errorhandler(ValidationError)
def validation_error(error):
    """Handle validation errors"""
    return jsonify({
        "error": "Validation error",
        "message": str(error),
        "status_code": 400,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 400

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with simple API documentation"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Profile REST API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #27ae60; font-weight: bold; }
            .url { color: #3498db; font-family: monospace; }
            .status { color: #e74c3c; font-weight: bold; }
            .test-btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .test-btn:hover { background: #2980b9; }
            .result { background: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px; font-family: monospace; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 User Profile REST API</h1>
            <p><strong>Status:</strong> <span style="color: #27ae60;">✅ Running & Healthy</span></p>
            <p><strong>Server Time:</strong> ''' + datetime.utcnow().isoformat() + '''Z</p>
            
            <h2>📡 Available Endpoints</h2>
            
            <div class="endpoint">
                <strong class="method">GET</strong> <span class="url">/api/health</span> - Health Check
                <button class="test-btn" onclick="testHealth()">Test</button>
                <div id="health-result" class="result" style="display:none;"></div>
            </div>
            
            <div class="endpoint">
                <strong class="method">GET</strong> <span class="url">/api/users</span> - Get All Users
                <button class="test-btn" onclick="testUsers()">Test</button>
                <div id="users-result" class="result" style="display:none;"></div>
            </div>
            
            <div class="endpoint">
                <strong class="method">GET</strong> <span class="url">/api/users/{id}</span> - Get User by ID
                <button class="test-btn" onclick="testUser()">Test (User 1)</button>
                <div id="user-result" class="result" style="display:none;"></div>
            </div>
        </div>

        <script>
            function testHealth() {
                const resultDiv = document.getElementById('health-result');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '🔄 Loading...';
                
                fetch('/api/health')
                    .then(response => response.json())
                    .then(data => {
                        resultDiv.innerHTML = '✅ Success:\n' + JSON.stringify(data, null, 2);
                        resultDiv.style.background = '#d4edda';
                    })
                    .catch(error => {
                        resultDiv.innerHTML = '❌ Error:\n' + error.message;
                        resultDiv.style.background = '#f8d7da';
                    });
            }
            
            function testUsers() {
                const resultDiv = document.getElementById('users-result');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '🔄 Loading...';
                
                fetch('/api/users')
                    .then(response => response.json())
                    .then(data => {
                        resultDiv.innerHTML = '✅ Success:\n' + JSON.stringify(data, null, 2);
                        resultDiv.style.background = '#d4edda';
                    })
                    .catch(error => {
                        resultDiv.innerHTML = '❌ Error:\n' + error.message;
                        resultDiv.style.background = '#f8d7da';
                    });
            }
            
            function testUser() {
                const resultDiv = document.getElementById('user-result');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '🔄 Loading...';
                
                fetch('/api/users/1')
                    .then(response => response.json())
                    .then(data => {
                        resultDiv.innerHTML = '✅ Success:\n' + JSON.stringify(data, null, 2);
                        resultDiv.style.background = '#d4edda';
                    })
                    .catch(error => {
                        resultDiv.innerHTML = '❌ Error:\n' + error.message;
                        resultDiv.style.background = '#f8d7da';
                    });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "API is running",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    try:
        # Return a list of users with basic info only (excluding sensitive data)
        users_list = []
        for user in USERS_DB.values():
            users_list.append({
                "id": user["id"],
                "username": user["username"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "created_at": user["created_at"]
            })
        
        return jsonify({
            "users": users_list,
            "count": len(users_list),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error fetching users: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to fetch users",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    """
    Get user profile by ID
    
    Args:
        user_id: The ID of the user (must be a positive integer)
    
    Returns:
        User profile information
    """
    try:
        # Validate user_id
        user_id = validate_user_id(user_id)
        
        # Check if user exists
        user = USERS_DB.get(user_id)
        if not user:
            return jsonify({
                "error": "User not found",
                "message": f"User with ID {user_id} does not exist",
                "status_code": 404,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }), 404
        
        # Return user profile (excluding sensitive data like email)
        user_profile = {
            "id": user["id"],
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "age": user["age"],
            "created_at": user["created_at"]
        }
        
        return jsonify({
            "user": user_profile,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
    
    except ValidationError as e:
        raise e
    except Exception as e:
        app.logger.error(f"Error fetching user {user_id}: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to fetch user profile",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Create a new user
    
    Expected JSON body:
    {
        "username": "string (required, min 3 chars)",
        "email": "string (required, valid email format)",
        "first_name": "string (required)",
        "last_name": "string (required)",
        "age": "integer (optional, 0-150)"
    }
    """
    try:
        # Check if request has JSON data
        if not request.is_json:
            raise BadRequest("Request must be in JSON format")
        
        data = request.get_json()
        if not data:
            raise BadRequest("Request body cannot be empty")
        
        # Validate required fields
        required_fields = ['username', 'email', 'first_name', 'last_name']
        missing_fields = []
        for field in required_fields:
            if not data.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            raise BadRequest(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate individual fields
        username = validate_username(data['username'])
        email = validate_email(data['email'])
        first_name = data['first_name'].strip()
        last_name = data['last_name'].strip()
        age = validate_age(data.get('age'))
        
        if not first_name:
            raise BadRequest("First name cannot be empty")
        if not last_name:
            raise BadRequest("Last name cannot be empty")
        
        # Check if username or email already exists
        for existing_user in USERS_DB.values():
            if existing_user['username'] == username:
                raise BadRequest("Username already exists")
            if existing_user['email'] == email:
                raise BadRequest("Email already exists")
        
        # Create new user
        new_user_id = max(USERS_DB.keys()) + 1
        new_user = {
            "id": new_user_id,
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        
        USERS_DB[new_user_id] = new_user
        
        # Return created user (excluding email for privacy)
        response_user = {
            "id": new_user["id"],
            "username": new_user["username"],
            "first_name": new_user["first_name"],
            "last_name": new_user["last_name"],
            "age": new_user["age"],
            "created_at": new_user["created_at"]
        }
        
        return jsonify({
            "message": "User created successfully",
            "user": response_user,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 201
    
    except (BadRequest, ValidationError):
        raise
    except Exception as e:
        app.logger.error(f"Error creating user: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to create user",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user
    
    Args:
        user_id: The ID of the user to update
    
    Expected JSON body (all fields optional):
    {
        "username": "string (min 3 chars)",
        "email": "string (valid email format)",
        "first_name": "string",
        "last_name": "string",
        "age": "integer (0-150)"
    }
    """
    try:
        # Validate user_id
        user_id = validate_user_id(user_id)
        
        # Check if user exists
        user = USERS_DB.get(user_id)
        if not user:
            return jsonify({
                "error": "User not found",
                "message": f"User with ID {user_id} does not exist",
                "status_code": 404,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }), 404
        
        # Check if request has JSON data
        if not request.is_json:
            raise BadRequest("Request must be in JSON format")
        
        data = request.get_json()
        if not data:
            raise BadRequest("Request body cannot be empty")
        
        # Update fields if provided
        if 'username' in data:
            new_username = validate_username(data['username'])
            # Check if new username already exists
            for existing_user in USERS_DB.values():
                if existing_user['username'] == new_username and existing_user['id'] != user_id:
                    raise BadRequest("Username already exists")
            user['username'] = new_username
        
        if 'email' in data:
            new_email = validate_email(data['email'])
            # Check if new email already exists
            for existing_user in USERS_DB.values():
                if existing_user['email'] == new_email and existing_user['id'] != user_id:
                    raise BadRequest("Email already exists")
            user['email'] = new_email
        
        if 'first_name' in data:
            first_name = data['first_name'].strip()
            if not first_name:
                raise BadRequest("First name cannot be empty")
            user['first_name'] = first_name
        
        if 'last_name' in data:
            last_name = data['last_name'].strip()
            if not last_name:
                raise BadRequest("Last name cannot be empty")
            user['last_name'] = last_name
        
        if 'age' in data:
            user['age'] = validate_age(data['age'])
        
        # Return updated user (excluding email for privacy)
        response_user = {
            "id": user["id"],
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "age": user["age"],
            "created_at": user["created_at"]
        }
        
        return jsonify({
            "message": "User updated successfully",
            "user": response_user,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
    
    except (BadRequest, ValidationError):
        raise
    except Exception as e:
        app.logger.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to update user",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user
    
    Args:
        user_id: The ID of the user to delete
    """
    try:
        # Validate user_id
        user_id = validate_user_id(user_id)
        
        # Check if user exists
        if user_id not in USERS_DB:
            return jsonify({
                "error": "User not found",
                "message": f"User with ID {user_id} does not exist",
                "status_code": 404,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }), 404
        
        # Delete user
        deleted_user = USERS_DB.pop(user_id)
        
        return jsonify({
            "message": "User deleted successfully",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
    
    except ValidationError as e:
        raise e
    except Exception as e:
        app.logger.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to delete user",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500

if __name__ == '__main__':
    # Run in debug mode for development
    app.run(host='0.0.0.0', port=5000, debug=True)