# Optimized Development Workflow

## Issue
VS Code was hanging due to heavy directories in the monorepo:
- `node_modules` (frontend and root)
- `.next` (Next.js build files)
- `__pycache__` (Python cache)
- `venv` (Python virtual environment)
- Various cache directories

## Solution Applied
All heavy directories were removed to improve VS Code performance. The `.gitignore` file already had proper entries to prevent these from being committed.

## Setup Instructions

### Quick Setup Script
Run the appropriate script for your OS:

**Windows:**
```cmd
setup_dev_environment.bat
```

**Linux/Mac:**
```bash
./setup_dev_environment.sh
```

### Manual Setup
If you prefer to set up manually:

#### Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Frontend (Next.js)
```bash
cd frontend
npm install
```

## Development Workflow
To avoid VS Code performance issues:

1. **Work on frontend only:** Open VS Code in the `frontend/` directory
2. **Work on backend only:** Open VS Code in the `backend/` directory
3. **Full project:** Only open the root directory when you specifically need to work on both simultaneously

## Running Applications Separately

### Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

## When to Recreate Dependencies
- If you encounter package-related errors
- After pulling updates that change dependencies
- Periodically to ensure clean installation

## Status
Both frontend and backend dependencies have been successfully installed:
- Frontend: Next.js v16.1.1 and all dependencies installed in frontend/node_modules
- Backend: All Python packages installed globally (also available in requirements.txt)

The dependencies will be ignored by git due to the .gitignore rules, so they won't be committed to the repository.