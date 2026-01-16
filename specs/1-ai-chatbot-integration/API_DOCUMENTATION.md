# AI Chatbot API Documentation

## Overview
The AI Chatbot API provides endpoints for interacting with an AI-powered assistant that can help manage your todo tasks using natural language.

## Authentication
All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Endpoints

### POST /api/{user_id}/chat
Send a message to the AI chatbot and receive a response.

#### Request
- **Method**: POST
- **Path**: `/api/{user_id}/chat`
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
  - `Content-Type: application/json`
- **Path Parameters**:
  - `user_id` (string): The ID of the authenticated user
- **Body**:
```json
{
  "message": "User's message to the chatbot",
  "conversation_id": 123 // Optional: existing conversation ID, if continuing
}
```

#### Response
- **Success (200 OK)**:
```json
{
  "conversation_id": 123,
  "response": "Assistant's response to the user",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "title": "Buy groceries",
        "description": "Milk, bread, eggs"
      },
      "result": {
        "task_id": 456,
        "status": "pending",
        "title": "Buy groceries"
      }
    }
  ],
  "timestamp": "2026-01-10T10:00:00Z"
}
```

- **Rate Limited (429)**: Too many requests
- **Unauthorized (401)**: Invalid or missing JWT token
- **Forbidden (403)**: User ID in token doesn't match path parameter
- **Bad Request (400)**: Invalid request body
- **Internal Server Error (500)**: Server error processing request

### GET /api/{user_id}/conversations
Retrieve a list of user's conversations.

#### Request
- **Method**: GET
- **Path**: `/api/{user_id}/conversations`
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Path Parameters**:
  - `user_id` (string): The ID of the authenticated user
- **Query Parameters**:
  - `limit` (integer, optional): Number of conversations to return (default: 10)
  - `offset` (integer, optional): Number of conversations to skip (default: 0)

#### Response
- **Success (200 OK)**:
```json
{
  "conversations": [
    {
      "id": 123,
      "title": "Grocery tasks",
      "created_at": "2026-01-10T09:00:00Z",
      "updated_at": "2026-01-10T10:00:00Z"
    }
  ],
  "total_count": 1
}
```

- **Rate Limited (429)**: Too many requests
- **Unauthorized (401)**: Invalid or missing JWT token
- **Forbidden (403)**: User ID in token doesn't match path parameter
- **Internal Server Error (500)**: Server error retrieving conversations

### GET /api/{user_id}/conversations/{conversation_id}/messages
Retrieve messages for a specific conversation.

#### Request
- **Method**: GET
- **Path**: `/api/{user_id}/conversations/{conversation_id}/messages`
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Path Parameters**:
  - `user_id` (string): The ID of the authenticated user
  - `conversation_id` (integer): The ID of the conversation
- **Query Parameters**:
  - `limit` (integer, optional): Number of messages to return (default: 50)
  - `offset` (integer, optional): Number of messages to skip (default: 0)

#### Response
- **Success (200 OK)**:
```json
{
  "messages": [
    {
      "id": 456,
      "sender_type": "user",
      "content": "Add a task to buy groceries",
      "timestamp": "2026-01-10T09:30:00Z",
      "tool_calls": []
    },
    {
      "id": 457,
      "sender_type": "assistant",
      "content": "I've added the task 'buy groceries' to your list.",
      "timestamp": "2026-01-10T09:30:05Z",
      "tool_calls": [
        {
          "tool_name": "add_task",
          "parameters": {
            "title": "buy groceries"
          },
          "result": {
            "task_id": 789,
            "status": "pending",
            "title": "buy groceries"
          }
        }
      ]
    }
  ],
  "total_count": 2
}
```

- **Rate Limited (429)**: Too many requests
- **Unauthorized (401)**: Invalid or missing JWT token
- **Forbidden (403)**: User ID in token doesn't match path parameter or conversation doesn't belong to user
- **Not Found (404)**: Conversation with given ID doesn't exist
- **Internal Server Error (500)**: Server error retrieving messages

## Rate Limits
- Chat endpoint: 10 requests per minute per IP
- Conversations endpoints: 20 requests per minute per IP

## Supported Commands
The AI assistant understands natural language commands to:
- Add tasks: "Add a task to buy groceries" or "Create a task to call mom"
- List tasks: "Show my tasks" or "What are my tasks?"
- Complete tasks: "Mark the grocery task as complete"
- Update tasks: "Change the grocery task to include milk"
- Delete tasks: "Delete the grocery task"