@echo off
REM Product Intelligence Auto-Update Script
REM Schedule this to run every hour using Windows Task Scheduler

echo ===============================================
echo Product Intelligence Auto-Update
echo ===============================================
echo Starting at %date% %time%

cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the update command
echo Running product intelligence update...
python manage.py update_product_intelligence --verbose

REM Check if update was successful
if %errorlevel% equ 0 (
    echo ✅ Product intelligence update completed successfully!
) else (
    echo ❌ Product intelligence update failed with error code %errorlevel%
)

echo ===============================================
echo Update completed at %date% %time%
echo ===============================================

REM Optional: Send notification (uncomment if you want)
REM echo Product intelligence update completed | msg %username%

pause
