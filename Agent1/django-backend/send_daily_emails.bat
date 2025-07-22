@echo off
echo Sending Daily Email Reports...
cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"
python manage.py send_scheduled_reports
echo Daily email reports completed at %date% %time%
