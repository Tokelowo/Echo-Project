@echo off
echo Sending Daily Email Reports...
cd /d "c:\Users\t-tokelowo\Documents\Echo Project\Agent1\django-backend"
python send_email_now.py
echo Daily email reports completed at %date% %time%
