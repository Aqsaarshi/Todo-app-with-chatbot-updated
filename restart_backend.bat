@echo off
echo Stopping any existing backend processes...
taskkill /f /im uvicorn.exe 2>nul

echo Starting the backend server...
cd backend
call venv\Scripts\activate.bat
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

echo Backend server started on port 8000
pause