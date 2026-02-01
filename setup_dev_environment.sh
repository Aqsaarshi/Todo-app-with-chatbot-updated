#!/bin/bash
echo "Setting up development environment..."
echo

echo "Installing backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "Backend setup complete!"
echo

echo "Installing frontend dependencies..."
cd ../frontend
npm install

echo
echo "Frontend setup complete!"
echo

echo "Development environment setup is complete!"
echo
echo "To run the backend: cd backend && source venv/bin/activate && uvicorn src.main:app --reload"
echo "To run the frontend: cd frontend && npm run dev"
echo