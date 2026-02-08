#!/bin/bash
# Script to build and run the Todo App with Chatbot

echo "Building and running Todo App with Docker..."

# Build and start the services
docker-compose -f docker-compose.fixed.yml up --build

echo "Services are now running!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"