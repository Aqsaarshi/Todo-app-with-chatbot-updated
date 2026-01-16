# Quickstart Guide: AI Todo Chatbot Integration

## Overview
This guide provides a quick introduction to the AI Todo Chatbot feature implementation, including setup instructions and key components.

## Prerequisites
- Python 3.11+ with pip
- Node.js 18+ with npm/yarn
- Access to Cohere API (COHERE_API_KEY)
- Neon PostgreSQL database setup
- Better Auth configured for user authentication

## Environment Setup

### Backend
1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export COHERE_API_KEY="your-cohere-api-key"
export DATABASE_URL="your-neon-db-url"
export JWT_SECRET="your-jwt-secret"
```

3. Run database migrations:
```bash
python -m alembic upgrade head
```

4. Start the backend server:
```bash
uvicorn src.main:app --reload
```

### Frontend
1. Install JavaScript dependencies:
```bash
cd frontend
npm install
```

2. Set environment variables in `.env.local`:
```bash
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api"
NEXT_PUBLIC_JWT_SECRET="your-jwt-secret"
```

3. Start the frontend development server:
```bash
npm run dev
```

## Key Components

### Backend Components
- `src/services/cohere_service.py`: Handles communication with Cohere API
- `src/tools/mcp_tools.py`: Defines MCP tools for task operations
- `src/api/chat.py`: Implements the chat endpoint
- `src/models/conversation.py`: Conversation data model
- `src/models/message.py`: Message data model

### Frontend Components
- `src/components/ChatBotIcon.tsx`: Floating chatbot icon component
- `src/components/ChatInterface.tsx`: Main chat interface component
- `src/services/apiClient.ts`: API client for chat endpoints

## API Endpoints
- `POST /api/{user_id}/chat`: Send message to chatbot
- `GET /api/{user_id}/conversations`: Get user's conversations
- `GET /api/{user_id}/conversations/{conversation_id}/messages`: Get messages for conversation

## Development Workflow
1. Make changes to backend or frontend
2. Test with the chat interface
3. Verify that Cohere correctly interprets commands and calls appropriate tools
4. Ensure all data is properly stored in the database
5. Verify JWT authentication is working correctly

## Testing
- Run backend tests: `pytest tests/`
- Run frontend tests: `npm test`
- Manual testing through the UI

## Troubleshooting
- If Cohere API calls fail, verify your API key is set correctly
- If authentication fails, check JWT token validity and secret
- If database operations fail, verify your connection string and run migrations