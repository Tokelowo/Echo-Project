@echo off
echo Starting React Development Server on Port 3001...
cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"
echo Current directory: %cd%
echo.
echo Installing dependencies (if needed)...
npm install
echo.
echo Starting development server...
npm run dev
echo.
echo Server should now be running at http://localhost:3001
pause
