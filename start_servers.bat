@echo off
echo Starting Todo App Servers...

REM Start backend in a new window
start "Backend Server" cmd /k "cd /d \"E:\hackathon-2TODOphase3 - Copy\backend\" && python -m uvicorn src.main:app --host 0.0.0.0 --port 7860"

REM Wait a bit for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in a new window
start "Frontend Server" cmd /k "cd /d \"E:\hackathon-2TODOphase3 - Copy\frontend\" && npm run dev"

echo Servers should be starting in separate windows.
echo Backend: http://localhost:7860
echo Frontend: http://localhost:3000
pause