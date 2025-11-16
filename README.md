# User Profile REST API

A simple REST API endpoint that returns user profile information with proper error handling and input validation.

## Features

- **CRUD Operations**: Create, Read, Update, Delete users
- **Input Validation**: Comprehensive validation for all user inputs
- **Error Handling**: Proper error responses with meaningful messages
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **Health Check**: Endpoint to check API status
- **JSON API**: RESTful API following JSON standards

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```
Returns the API health status.

### Get All Users
```
GET /api/users
```
Returns a list of all users with basic information.

### Get User Profile
```
GET /api/users/{user_id}
```
Returns detailed profile information for a specific user.

**Path Parameters:**
- `user_id` (required): The ID of the user (must be a positive integer)

### Create User
```
POST /api/users
```
Creates a new user.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "age": 30
}
```

**Validation Rules:**
- `username`: Required, minimum 3 characters, alphanumeric and underscores only
- `email`: Required, valid email format
- `first_name`: Required, cannot be empty
- `last_name`: Required, cannot be empty
- `age`: Optional, must be between 0-150

### Update User
```
PUT /api/users/{user_id}
```
Updates an existing user.

**Path Parameters:**
- `user_id` (required): The ID of the user to update

**Request Body:** (All fields optional)
```json
{
  "username": "new_username",
  "email": "new.email@example.com",
  "first_name": "NewFirst",
  "last_name": "NewLast",
  "age": 31
}
```

### Delete User
```
DELETE /api/users/{user_id}
```
Deletes a user.

**Path Parameters:**
- `user_id` (required): The ID of the user to delete

## Error Responses

All error responses follow this format:
```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "status_code": 400,
  "timestamp": "2023-11-16T20:51:00Z"
}
```

### Common Error Types

- **400 Bad Request**: Invalid input data, missing required fields
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error
- **Validation Error**: Input validation failed

## Input Validation

The API includes comprehensive input validation:

### User ID Validation
- Must be a valid positive integer
- Must be greater than 0

### Username Validation
- Required field
- Minimum 3 characters
- Can only contain letters, numbers, and underscores
- Must be unique

### Email Validation
- Required field
- Must be valid email format
- Must be unique

### Name Validation
- Required fields (first_name, last_name)
- Cannot be empty strings
- Leading/trailing whitespace is trimmed

### Age Validation
- Optional field
- Must be between 0-150
- Must be a valid number

## Sample Usage

### Get User Profile
```bash
curl -X GET "http://localhost:5000/api/users/1"
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "created_at": "2023-01-15T10:30:00Z"
  },
  "timestamp": "2023-11-16T20:51:00Z"
}
```

### Create New User
```bash
curl -X POST "http://localhost:5000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_wonder",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Wonder",
    "age": 25
  }'
```

### Update User
```bash
curl -X PUT "http://localhost:5000/api/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 31
  }'
```

### Delete User
```bash
curl -X DELETE "http://localhost:5000/api/users/1"
```

## Error Handling Examples

### Invalid User ID
```bash
curl -X GET "http://localhost:5000/api/users/invalid"
```

**Response:**
```json
{
  "error": "Validation error",
  "message": "User ID must be a valid integer",
  "status_code": 400,
  "timestamp": "2023-11-16T20:51:00Z"
}
```

### Missing Required Fields
```bash
curl -X POST "http://localhost:5000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test"
  }'
```

**Response:**
```json
{
  "error": "Bad request",
  "message": "Missing required fields: email, first_name, last_name",
  "status_code": 400,
  "timestamp": "2023-11-16T20:51:00Z"
}
```

### User Not Found
```bash
curl -X GET "http://localhost:5000/api/users/999"
```

**Response:**
```json
{
  "error": "User not found",
  "message": "User with ID 999 does not exist",
  "status_code": 404,
  "timestamp": "2023-11-16T20:51:00Z"
}
```

## Testing

You can test the API using curl commands as shown in the examples above, or use tools like Postman or Insomnia.

## Security Notes

- Email addresses are stored but not returned in API responses for privacy
- Input validation prevents SQL injection and other common attacks
- CORS is enabled for cross-origin requests
- In a production environment, consider adding:
  - Authentication and authorization
  - Rate limiting
  - Input sanitization
  - HTTPS
  - API key management