#!/usr/bin/env python
"""
Django Backend Server Startup Script
"""
import os
import sys
import subprocess

def main():
    # Change to the Django backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    print("Starting Django Backend Server...")
    print(f"Working directory: {backend_dir}")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    try:
        # Check if Django is installed
        import django
        print(f"Django version: {django.get_version()}")
        
        # Import Django management
        from django.core.management import execute_from_command_line
        
        # Run migrations first
        print("\nRunning migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Start the server
        print("\nStarting Django development server...")
        print("Backend will be available at: http://127.0.0.1:8000")
        print("API Overview endpoint: http://127.0.0.1:8000/research-agent/overview/")
        print("\nPress Ctrl+C to stop the server")
        
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
        
    except ImportError as exc:
        print(f"Error: {exc}")
        print("Django is not installed or not available.")
        print("Please install Django with: pip install django djangorestframework django-cors-headers")
        sys.exit(1)
    except Exception as exc:
        print(f"Error starting server: {exc}")
        sys.exit(1)

if __name__ == '__main__':
    main()
