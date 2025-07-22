@echo off
title React Frontend Server  
echo.
echo 🌐 STARTING REACT FRONTEND SERVER
echo ==================================
echo.
echo Frontend will be available at: http://localhost:3000
echo.

cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"

echo Checking Node.js setup...
node --version
npm --version
echo.

echo 🚀 Starting React development server...
echo.
echo IMPORTANT: Keep this window open while using the app
echo Your browser should automatically open to http://localhost:3000
echo.

npm run dev

echo.
echo ⚠️  Server stopped. Press any key to close...
pause
