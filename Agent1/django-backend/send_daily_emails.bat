@echo off
echo Sending Daily Email Reports...
cd /d "c:\Users\t-tokelowo\Documents\Echo Project\Agent1\django-backend"
python manage.py send_scheduled_reports
echo Daily email reports completed at %date% %time%
