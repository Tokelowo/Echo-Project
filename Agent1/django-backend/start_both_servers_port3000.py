#!/usr/bin/env python
"""
Start both Django and React servers with Django on port 3000
"""
import subprocess
import sys
import time
import os

def start_servers():
    print("🚀 Starting Django Backend on Port 3000 and React Frontend")
    print("=" * 60)
    
    # Change to Django directory
    django_dir = r"c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"
    react_dir = r"c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"
    
    print("1️⃣ Starting Django Backend Server on port 3000...")
    
    # Start Django server
    django_cmd = [sys.executable, 'manage.py', 'runserver', '3000']
    try:
        django_process = subprocess.Popen(
            django_cmd, 
            cwd=django_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print("✅ Django server starting on http://127.0.0.1:3000")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Error starting Django: {e}")
        return
    
    print("\n2️⃣ Starting React Frontend Server...")
    
    # Start React server
    react_cmd = ['npm', 'run', 'dev']
    try:
        react_process = subprocess.Popen(
            react_cmd, 
            cwd=react_dir,
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print("✅ React server starting on http://localhost:5173")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Error starting React: {e}")
        return
    
    print("\n🎉 Both servers are starting!")
    print("⏳ Wait 10-15 seconds for full startup")
    print("🌐 Then open: http://localhost:5173")
    print("📊 Navigate to Market Trends to see REAL data!")
    print("\n🔧 Server Configuration:")
    print("   Django Backend: http://127.0.0.1:3000")
    print("   React Frontend: http://localhost:5173")
    print("   API calls now use port 3000")

if __name__ == "__main__":
    start_servers()
