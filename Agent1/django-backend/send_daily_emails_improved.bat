@echo off
echo ===============================================
echo DAILY EMAIL SYSTEM - Running at %date% %time%
echo ===============================================

cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"

echo Checking Django environment...
python manage.py check --deploy

echo.
echo Sending scheduled email reports...
python manage.py send_scheduled_reports

echo.
echo Email task completed at %date% %time%
echo ===============================================
