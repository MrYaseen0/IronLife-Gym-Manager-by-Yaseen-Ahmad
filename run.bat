@echo off
REM IronLife Gym Manager - Startup Script

echo.
echo ======================================
echo   IRONLIFE GYM MANAGER
echo   Startup Script
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Flask not installed. Installing requirements...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
)

echo [OK] Requirements installed
echo.

REM Kill any existing Python processes on port 5000
echo Cleaning up old processes...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000"') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo ======================================
echo   Starting Backend Server...
echo ======================================
echo.
echo The server will start on: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask app
python app.py

pause
