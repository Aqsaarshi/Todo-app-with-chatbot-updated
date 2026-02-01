@echo off
echo Setting up development environment...
echo.

echo Installing backend dependencies...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python packages...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Backend setup complete!
echo.

echo Installing frontend dependencies...
cd ..\frontend
npm install

echo.
echo Frontend setup complete!
echo.

echo Development environment setup is complete!
echo.
echo To run the backend: cd backend && venv\Scripts\activate && uvicorn src.main:app --reload
echo To run the frontend: cd frontend && npm run dev
echo.
pause