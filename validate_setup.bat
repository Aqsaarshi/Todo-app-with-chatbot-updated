@echo off
REM Validation script to check if the Todo App services are running correctly

echo Validating Todo App Setup...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo ✓ Docker is running

REM Check if the containers are running
echo Checking running containers...
for /f "tokens=*" %%i in ('docker ps --format "table {{.Names}}\t{{.Status}}"') do (
    set "container_line=%%i"
    if "!container_line!" neq "NAMES    STATUS" (
        if "!container_line!" neq "" (
            echo !container_line!
            if "!container_line!" equ "todo-backend" (
                echo ✓ Backend container is running
            )
            if "!container_line!" equ "todo-frontend" (
                echo ✓ Frontend container is running
            )
            if "!container_line!" equ "todo-postgres" (
                echo ✓ Database container is running
            )
        )
    )
)

echo.
echo Testing service accessibility...

REM Test backend using PowerShell for curl-like functionality
powershell -Command "try { $response = Invoke-WebRequest -Uri http://localhost:8000/health -TimeoutSec 5; if ($response.StatusCode -eq 200) { Write-Host '✓ Backend API is accessible at http://localhost:8000/health' } } catch { Write-Host '⚠ Backend API may not be accessible at http://localhost:8000' }"

REM Test frontend using PowerShell for curl-like functionality
powershell -Command "try { $response = Invoke-WebRequest -Uri http://localhost:3000 -TimeoutSec 5; if ($response.StatusCode -eq 200) { Write-Host '✓ Frontend is accessible at http://localhost:3000' } } catch { Write-Host '⚠ Frontend may not be accessible at http://localhost:3000' }"

echo.
echo Validation complete!
echo.
echo Services should be available at:
echo   - Frontend: http://localhost:3000
echo   - Backend: http://localhost:8000
echo   - Backend API Docs: http://localhost:8000/docs

pause