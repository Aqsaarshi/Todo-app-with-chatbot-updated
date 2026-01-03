# API Contract: Todo Full-Stack Web Application

**Version**: 1.0.0
**Date**: 2025-12-27
**Feature**: 002-todo-fullstack-web-app

## Authentication API

### Register User
- **Endpoint**: `POST /api/auth/register`
- **Description**: Register a new user account
- **Authentication**: None required

#### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

#### Response (200 OK)
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "User registered successfully"
}
```

#### Response (400 Bad Request)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format or password too weak"
  }
}
```

### Login User
- **Endpoint**: `POST /api/auth/login`
- **Description**: Authenticate user and return JWT token
- **Authentication**: None required

#### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

#### Response (200 OK)
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login successful"
}
```

### Logout User
- **Endpoint**: `POST /api/auth/logout`
- **Description**: Invalidate user session
- **Authentication**: JWT token required in Authorization header

#### Request Headers
```
Authorization: Bearer <jwt_token>
```

#### Response (200 OK)
```json
{
  "message": "Logout successful"
}
```

## Task Management API

### Get User Tasks
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Description**: Retrieve all tasks for a specific user
- **Authentication**: Valid JWT token required

#### Query Parameters
- `completed` (optional): Filter by completion status (true/false)
- `priority` (optional): Filter by priority (low, medium, high)
- `sort` (optional): Sort field (created_at, due_date, priority, title)
- `order` (optional): Sort order (asc, desc)

#### Response (200 OK)
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Complete project proposal",
      "description": "Finish and submit the project proposal document",
      "completed": false,
      "priority": "high",
      "due_date": "2025-12-31T10:00:00Z",
      "created_at": "2025-12-27T15:30:00Z",
      "updated_at": "2025-12-27T15:30:00Z"
    }
  ]
}
```

### Create Task
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Description**: Create a new task for the user
- **Authentication**: Valid JWT token required

#### Request Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "due_date": "2025-12-28T18:00:00Z"
}
```

#### Response (201 Created)
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "priority": "medium",
    "due_date": "2025-12-28T18:00:00Z",
    "created_at": "2025-12-27T16:00:00Z",
    "updated_at": "2025-12-27T16:00:00Z"
  }
}
```

### Get Specific Task
- **Endpoint**: `GET /api/{user_id}/tasks/{id}`
- **Description**: Retrieve a specific task by ID
- **Authentication**: Valid JWT token required

#### Response (200 OK)
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "priority": "medium",
    "due_date": "2025-12-28T18:00:00Z",
    "created_at": "2025-12-27T16:00:00Z",
    "updated_at": "2025-12-27T16:00:00Z"
  }
}
```

### Update Task
- **Endpoint**: `PUT /api/{user_id}/tasks/{id}`
- **Description**: Update task details
- **Authentication**: Valid JWT token required

#### Request Body (all fields optional)
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "completed": false,
  "priority": "high",
  "due_date": "2025-12-28T20:00:00Z"
}
```

#### Response (200 OK)
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries and cook dinner",
    "description": "Milk, eggs, bread, chicken",
    "completed": false,
    "priority": "high",
    "due_date": "2025-12-28T20:00:00Z",
    "created_at": "2025-12-27T16:00:00Z",
    "updated_at": "2025-12-27T16:30:00Z"
  }
}
```

### Delete Task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{id}`
- **Description**: Delete a specific task
- **Authentication**: Valid JWT token required

#### Response (200 OK)
```json
{
  "message": "Task deleted successfully"
}
```

### Toggle Task Completion
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`
- **Description**: Toggle task completion status
- **Authentication**: Valid JWT token required

#### Request Body
```json
{
  "completed": true
}
```

#### Response (200 OK)
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "completed": true
  }
}
```

## Error Response Format

All error responses follow this standard format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if applicable"
  }
}
```

### Common Error Codes
- `AUTHENTICATION_REQUIRED`: Missing or invalid JWT token
- `FORBIDDEN_ACCESS`: User trying to access another user's data
- `VALIDATION_ERROR`: Request body validation failed
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `INTERNAL_SERVER_ERROR`: Unexpected server error