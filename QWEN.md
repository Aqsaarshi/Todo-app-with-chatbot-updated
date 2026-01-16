# Qwen Agent Context: AI Todo Chatbot Integration

## Overview
This file provides context for the Qwen AI agent about the AI Todo Chatbot feature implementation.

## Feature Context
The AI Todo Chatbot feature integrates natural language processing into the existing Todo application, allowing users to manage tasks via conversational interface. The implementation uses Cohere API for language understanding and MCP tools for task operations.

## Technologies Used
- **Cohere API**: Used for natural language processing and response generation
- **MCP (Model Context Protocol) Tools**: Used for structured function calling from the LLM
- **FastAPI**: Backend framework for API endpoints
- **SQLModel**: ORM for database operations
- **Neon PostgreSQL**: Cloud database service
- **Next.js 16+**: Frontend framework
- **Better Auth**: Authentication system
- **TypeScript/JavaScript**: Frontend programming languages

## Key Patterns
- **Stateless Server Architecture**: No in-memory session data; conversation history retrieved from database for each request
- **JWT Authentication**: All endpoints require JWT tokens for user identification
- **User Data Isolation**: All operations are scoped to the authenticated user
- **Event Sourcing for Conversations**: Messages stored as immutable events in chronological order

## Important Files
- `backend/src/services/cohere_service.py`: Cohere API integration
- `backend/src/tools/mcp_tools.py`: MCP tools definitions
- `backend/src/api/chat.py`: Chat endpoint implementation
- `frontend/src/components/ChatBotIcon.tsx`: Chatbot UI component
- `frontend/src/components/ChatInterface.tsx`: Chat interface implementation

## Security Considerations
- All API endpoints require JWT authentication
- User data is isolated by user_id in all database queries
- Input validation is performed on all user inputs
- API keys are stored in environment variables

## Performance Considerations
- Database queries are optimized with appropriate indexing
- Cohere API calls are asynchronous to prevent blocking
- Conversation history is paginated to prevent overly large responses

## Testing Approach
- Unit tests for individual components
- Integration tests for API endpoints
- End-to-end tests for complete user flows
- Mocking of external services (Cohere API) for testing