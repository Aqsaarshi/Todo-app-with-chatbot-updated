@echo off
REM Script to build Docker images for todo-new-backend and todo-new-frontend

echo Building Docker images for Todo App...

echo.
echo Building todo-new-backend image...
docker build -t todo-new-backend ./backend
if %errorlevel% neq 0 (
    echo Failed to build todo-new-backend image
    pause
    exit /b %errorlevel%
)

echo.
echo Building todo-new-frontend image...
docker build -t todo-new-frontend ./frontend
if %errorlevel% neq 0 (
    echo Failed to build todo-new-frontend image
    pause
    exit /b %errorlevel%
)

echo.
echo Successfully built Docker images:
echo - todo-new-backend
echo - todo-new-frontend
echo.
echo To run the containers:
echo docker run -d -p 8000:8000 --name todo-backend-app todo-new-backend
echo docker run -d -p 3000:3000 --name todo-frontend-app todo-new-frontend
echo.
pause