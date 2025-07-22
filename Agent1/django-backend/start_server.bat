@echo off
echo Starting Django Backend Server...
echo.

REM Set Django environment variables
set DJANGO_SETTINGS_MODULE=backend.settings

REM Load .env file variables manually
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if not "%%a"=="" if not "%%a:~0,1%"=="#" (
        set "%%a=%%b"
    )
)

REM Start Django development server
echo Environment loaded. Starting server on http://127.0.0.1:8000
python manage.py runserver 127.0.0.1:8000

pause
