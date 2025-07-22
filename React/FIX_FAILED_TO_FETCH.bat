@echo off
echo 🚀 FIXING "Failed to fetch" ERRORS - STARTING DJANGO BACKEND
echo.
echo This will start the Django server at 127.0.0.1:8000
echo Keep this window open while using your React app!
echo.

cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"

if not exist "manage.py" (
    echo ❌ ERROR: manage.py not found
    echo Please check if Django backend is in the correct location
    pause
    exit /b 1
)

echo ✅ Starting Django server...
echo ✅ This will fix all API connection errors
echo.

python manage.py runserver 127.0.0.1:8000

pause
