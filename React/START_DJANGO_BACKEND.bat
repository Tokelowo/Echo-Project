@echo off
title Django Backend Server
echo.
echo 🚀 STARTING DJANGO BACKEND SERVER
echo ===================================
echo.
echo Backend will be available at: http://127.0.0.1:8000
echo React frontend expects: http://127.0.0.1:8000/research-agent/
echo.

cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"

echo Checking Django setup...
python --version
echo.

echo Testing Django configuration...
python manage.py check --deploy
echo.

if %ERRORLEVEL% EQU 0 (
    echo ✅ Django configuration is valid
    echo.
    echo 🚀 Starting Django development server...
    echo.
    echo IMPORTANT: Keep this window open while using the React app
    echo Close this window to stop the backend server
    echo.
    python manage.py runserver 127.0.0.1:8000
) else (
    echo ❌ Django configuration has errors
    echo.
    echo Trying to start anyway...
    python manage.py runserver 127.0.0.1:8000
)

echo.
echo ⚠️  Server stopped. Press any key to close...
pause
