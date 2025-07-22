@echo off
echo Starting Django Backend Server...
echo.

cd /d "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"

echo Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Virtual environment not found. Using system Python.
)

echo.
echo Installing/updating dependencies...
pip install django djangorestframework django-cors-headers python-dotenv requests beautifulsoup4 praw textblob lxml html5lib

echo.
echo Running Django migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Starting Django development server...
echo Backend will be available at: http://127.0.0.1:8000
echo API Overview endpoint: http://127.0.0.1:8000/research-agent/overview/
echo.

python manage.py runserver 127.0.0.1:8000

pause
