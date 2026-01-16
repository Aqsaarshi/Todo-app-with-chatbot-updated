#!/bin/bash
# Script to restart the backend server with the fixes

echo "Stopping any existing backend processes..."
pkill -f "uvicorn" || true

echo "Starting the backend server..."
cd backend
source venv/Scripts/activate  # Use venv/bin/activate on Linux/Mac
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

echo "Backend server started on port 8000"