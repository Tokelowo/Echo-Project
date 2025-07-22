@echo off
echo Setting up Windows Task Scheduler for Daily Emails...
echo.

set TASK_NAME="Daily Email Reports"
set BATCH_FILE="c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend\send_daily_emails.bat"
set SCHEDULE_TIME="09:00"

echo Creating scheduled task: %TASK_NAME%
echo Batch file: %BATCH_FILE%
echo Time: %SCHEDULE_TIME% daily
echo.

schtasks /create /tn %TASK_NAME% /tr %BATCH_FILE% /sc daily /st %SCHEDULE_TIME% /f

if %errorlevel% == 0 (
    echo ✅ Task created successfully!
    echo.
    echo To verify the task was created:
    echo   schtasks /query /tn %TASK_NAME%
    echo.
    echo To run the task manually:
    echo   schtasks /run /tn %TASK_NAME%
    echo.
    echo To delete the task:
    echo   schtasks /delete /tn %TASK_NAME% /f
) else (
    echo ❌ Failed to create task. You may need to run as Administrator.
)

pause
