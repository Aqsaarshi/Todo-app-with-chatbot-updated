# Quickstart Guide: Todo Full-Stack Web Application

**Date**: 2025-12-27
**Feature**: 002-todo-fullstack-web-app

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL (or access to Neon PostgreSQL)
- Docker and Docker Compose (for containerized setup)
- Git for version control

## Project Setup

### 1. Clone and Initialize Repository
```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and auth settings
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API endpoints and auth settings
```

## Database Setup

### 1. Database Initialization
```bash
# From backend directory
cd backend

# Run database migrations
alembic upgrade head
```

### 2. Environment Variables
Create `.env` file in the backend directory:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
NEON_DATABASE_URL=your_neon_database_url
SECRET_KEY=your_secret_key_for_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

### 1. Running Backend (Development)
```bash
# From backend directory
cd backend
source venv/bin/activate  # Activate virtual environment

# Run the backend server
uvicorn src.main:app --reload --port 8000
```

### 2. Running Frontend (Development)
```bash
# From frontend directory
cd frontend

# Run the frontend development server
npm run dev
# or
yarn dev
```

### 3. Running with Docker Compose
```bash
# From project root
docker-compose up --build
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Task Management
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Environment Configuration

### Frontend Environment Variables
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_COOKIE_NAME=auth_token
```

### Backend Environment Variables
```
DATABASE_URL=postgresql://localhost:5432/todo_app
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Testing

### Backend Tests
```bash
# From backend directory
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
# From frontend directory
cd frontend
npm test
# or
yarn test
```

## Deployment

### Building for Production
```bash
# Frontend build
cd frontend
npm run build

# Backend deployment
cd backend
# Deploy using your preferred platform (Heroku, AWS, etc.)
```

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure PostgreSQL is running and credentials are correct
2. **Port Conflicts**: Check if ports 3000 (frontend) and 8000 (backend) are available
3. **Environment Variables**: Verify all required environment variables are set

### Useful Commands
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check frontend build
cd frontend && npm run build && npm start
```