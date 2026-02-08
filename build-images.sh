#!/bin/bash
# Script to build Docker images for todo-new-backend and todo-new-frontend

echo "Building Docker images for Todo App..."

echo
echo "Building todo-new-backend image..."
docker build -t todo-new-backend ./backend
if [ $? -ne 0 ]; then
    echo "Failed to build todo-new-backend image"
    exit 1
fi

echo
echo "Building todo-new-frontend image..."
docker build -t todo-new-frontend ./frontend
if [ $? -ne 0 ]; then
    echo "Failed to build todo-new-frontend image"
    exit 1
fi

echo
echo "Successfully built Docker images:"
echo "- todo-new-backend"
echo "- todo-new-frontend"
echo
echo "To run the containers:"
echo "docker run -d -p 8000:8000 --name todo-backend-app todo-new-backend"
echo "docker run -d -p 3000:3000 --name todo-frontend-app todo-new-frontend"