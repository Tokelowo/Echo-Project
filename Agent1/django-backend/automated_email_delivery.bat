@echo off
cd /d "c:\Users\t-tokelowo\Documents\Echo Project\Agent1\django-backend"
python manage.py send_scheduled_reports
echo Email delivery completed at %date% %time%
