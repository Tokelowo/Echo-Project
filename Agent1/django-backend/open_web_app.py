#!/usr/bin/env python
"""
Start both servers and open the web app
"""
import subprocess
import sys
import time
import webbrowser
import os

def start_servers_and_open_app():
    print("🚀 Starting Real Market Trends Web Application")
    print("=" * 60)
    
    try:
        # Start Django backend on port 3000
        print("1️⃣ Starting Django Backend Server on port 3000...")
        backend_dir = r"c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"
        backend_process = subprocess.Popen([
            'powershell', '-Command', f'cd "{backend_dir}"; python manage.py runserver 3000'
        ], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        print("   ✅ Django backend starting...")
        time.sleep(3)
        
        # Start React frontend
        print("2️⃣ Starting React Frontend Server...")
        frontend_dir = r"c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"
        frontend_process = subprocess.Popen([
            'powershell', '-Command', f'cd "{frontend_dir}"; npm run dev'
        ], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        print("   ✅ React frontend starting...")
        time.sleep(8)  # Give React more time to start
        
        # Open the web application
        print("3️⃣ Opening Web Application...")
        print("   🌐 URL: http://localhost:3001")
        webbrowser.open('http://localhost:3001')
        
        print("\n🎯 SUCCESS!")
        print("=" * 60)
        print("✅ Django Backend: http://127.0.0.1:3000")
        print("✅ React Frontend: http://localhost:3001")
        print("✅ Browser opened automatically")
        print("\n📊 Navigate to 'Market Trends' to see REAL DATA:")
        print("   • Real market size calculations")
        print("   • Real MDO market share data")
        print("   • Real threat volume metrics")
        print("   • Real AI adoption rates")
        print("\n🔧 Servers are running in separate console windows")
        print("   Close those windows to stop the servers")
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting servers: {e}")
        return False

if __name__ == "__main__":
    start_servers_and_open_app()
    input("\nPress Enter to exit...")
