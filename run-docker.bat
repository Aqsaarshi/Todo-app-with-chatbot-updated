@echo off
REM Batch script to build and run the Todo App with Docker

echo Building and running Todo App with Docker...

REM Build and start the services
docker-compose -f docker-compose.fixed.yml up --build

echo Services are now running!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
pause