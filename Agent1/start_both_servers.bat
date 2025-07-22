@echo off
echo 🚀 Starting Django Backend and React Frontend
echo ================================================

echo.
echo 📍 Step 1: Starting Django Backend Server...
echo Backend will run on: http://127.0.0.1:8000
echo.

cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"

echo Checking Django configuration...
python manage.py check

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Django configuration has errors. Please fix them first.
    pause
    exit /b 1
)

echo ✅ Django configuration OK
echo.
echo Starting Django server...
echo 📊 API endpoints will be available at:
echo    - Overview: http://127.0.0.1:8000/research-agent/overview/
echo    - Competitive Metrics: http://127.0.0.1:8000/research-agent/competitive-metrics/
echo    - Customer Reviews: http://127.0.0.1:8000/research-agent/customer-reviews/
echo    - Market Intelligence: http://127.0.0.1:8000/research-agent/market-intelligence/
echo.
echo ⚠️  Keep this window open - Django server is running
echo 🔗 CORS configured for React ports: 3000-3005
echo.

start "Django Backend" cmd /k "python manage.py runserver 8000"

echo.
echo 📍 Step 2: Starting React Frontend...
echo Frontend should run on ports 3000-3005
echo.

timeout /t 3 /nobreak >nul

cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"

echo 📦 Installing React dependencies (if needed)...
call npm install

echo.
echo 🎯 Starting React development server...
echo The React app will open in your browser automatically
echo API calls are configured to connect to Django on port 8000
echo.

start "React Frontend" cmd /k "npm run dev"

echo.
echo ✅ BOTH SERVERS STARTING!
echo ================================
echo 📍 Django Backend: http://127.0.0.1:8000
echo 📍 React Frontend: Will be shown in the new window
echo.
echo 💡 If you still see "Failed to fetch" errors:
echo    1. Wait for both servers to fully start
echo    2. Check the terminal windows for any error messages
echo    3. Run: python connection_test.py to diagnose issues
echo.
echo 🔧 Fixed Issues:
echo    ✅ API base URL changed from port 3000 to 8000
echo    ✅ CORS settings updated for ports 3000-3005
echo    ✅ All React components updated with correct backend URL
echo.
pause
