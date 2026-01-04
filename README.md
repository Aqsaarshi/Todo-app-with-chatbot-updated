# Todo Full-Stack Web Application

A full-featured todo application with user authentication, task management, and responsive UI built with Next.js, FastAPI, and PostgreSQL.

## Features

- User authentication with JWT tokens
- Create, read, update, and delete tasks
- Task filtering and sorting
- User data isolation
- Responsive design
- Secure API endpoints

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL with SQLModel ORM
- **Authentication**: JWT-based with custom implementation
- **Deployment**: Docker and docker-compose

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (or access to Neon PostgreSQL)
- Docker and Docker Compose (for containerized setup)
- Git for version control

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials and auth settings
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.local.example .env.local
# Edit .env.local with your API endpoints and auth settings
```

4. Start the frontend development server:
```bash
npm run dev
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

## Environment Variables

### Frontend
```
NEXT_PUBLIC_API_URL=https://aqsaarshi-todo-app-backend.hf.space
NEXT_PUBLIC_AUTH_COOKIE_NAME=auth_token
```

### Backend
```
DATABASE_URL=postgresql://localhost:5432/todo_app
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running with Docker

To run the application using Docker Compose:

```bash
docker-compose up --build
```

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
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

## Security Features

- JWT token validation on all protected endpoints
- User ownership validation for all data access
- Input validation and sanitization
- Rate limiting for API endpoints (not implemented in this version)
- Data isolation between users

## Architecture

The application follows a monorepo structure with separate frontend and backend applications:

```
hackathon-todo/
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/       # Reusable UI components
│   │   ├── lib/              # Utilities and services
│   │   ├── types/            # TypeScript type definitions
│   │   └── styles/           # Global styles
│   └── ...
├── backend/
│   ├── src/
│   │   ├── models/           # SQLModel database models
│   │   ├── services/         # Business logic
│   │   ├── api/              # API routes/endpoints
│   │   ├── auth/             # Authentication logic
│   │   └── database/         # Database connection and setup
│   └── ...
└── ...
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Specify your license here]
# Todo-Full-Stack-Web-Application
