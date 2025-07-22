#!/usr/bin/env python
"""
Quick Start Guide for Real Market Trends Data System
"""
import os
import subprocess
import sys
import time
import webbrowser

def main():
    print("=" * 80)
    print("🚀 REAL MARKET TRENDS DATA - QUICK START GUIDE")
    print("=" * 80)
    print()
    
    print("📋 MANUAL STARTUP INSTRUCTIONS:")
    print("-" * 50)
    print()
    
    print("1️⃣ START DJANGO BACKEND:")
    print("   Open Command Prompt and run:")
    print("   cd \"c:\\Users\\t-tokelowo\\OneDrive - Microsoft\\Agent 1\\django-backend\"")
    print("   python manage.py runserver 3000")
    print("   ✅ Backend will be available at: http://127.0.0.1:3000")
    print()
    
    print("2️⃣ START REACT FRONTEND:")
    print("   Open another Command Prompt and run:")
    print("   cd \"c:\\Users\\t-tokelowo\\OneDrive - Microsoft\\Attachments\\React\"")
    print("   npm run dev")
    print("   ✅ Frontend will be available at: http://localhost:5173")
    print()
    
    print("3️⃣ TEST REAL DATA:")
    print("   🌐 Open browser: http://localhost:5173")
    print("   📊 Navigate to 'Market Trends' page")
    print("   🎯 See REAL data instead of hardcoded values!")
    print()
    
    print("🔧 ALTERNATIVE - USE BATCH FILES:")
    print("-" * 50)
    print("✅ Backend: Double-click start_backend.bat")
    print("✅ Frontend: Double-click start_frontend.bat")
    print()
    
    print("📊 WHAT YOU'LL SEE (REAL DATA):")
    print("-" * 50)
    print("✅ Market Size 2025: Real calculation from news analysis")
    print("✅ MDO Market Share: Real vendor mention percentages")
    print("✅ Threat Volume: Real threat activity from articles")
    print("✅ AI Adoption: Real AI security adoption metrics")
    print("✅ Data source information and confidence scores")
    print()
    
    print("🎯 VERIFICATION ENDPOINTS:")
    print("-" * 50)
    print("📡 Test backend directly:")
    print("   http://127.0.0.1:3000/research-agent/real-market-trends-data/")
    print("📡 Test product intelligence:")
    print("   http://127.0.0.1:3000/research-agent/product-intelligence/")
    print("📡 Test overview data:")
    print("   http://127.0.0.1:3000/research-agent/overview/")
    print()
    
    print("🚫 WHAT'S BEEN ELIMINATED:")
    print("-" * 50)
    print("❌ Hardcoded $5.8B market size")
    print("❌ Hardcoded 40% market share")
    print("❌ Hardcoded +58% threat volume")
    print("❌ Hardcoded 85% AI adoption")
    print("✅ ALL REPLACED WITH REAL, DATA-DRIVEN METRICS!")
    print()
    
    # Try to open batch files automatically
    backend_bat = r"c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend\start_backend.bat"
    frontend_bat = r"c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React\start_frontend.bat"
    
    print("🎮 QUICK START OPTIONS:")
    print("-" * 50)
    user_choice = input("Would you like me to open the startup batch files? (y/n): ").lower().strip()
    
    if user_choice == 'y':
        try:
            print("🚀 Opening Django backend startup...")
            subprocess.Popen(['cmd', '/c', 'start', backend_bat], shell=True)
            time.sleep(2)
            
            print("🚀 Opening React frontend startup...")
            subprocess.Popen(['cmd', '/c', 'start', frontend_bat], shell=True)
            time.sleep(2)
            
            print("✅ Both servers should now be starting!")
            print("⏳ Wait 10-15 seconds for servers to fully start")
            print("🌐 Then open: http://localhost:5173")
            
        except Exception as e:
            print(f"❌ Could not auto-start: {e}")
            print("📋 Please use manual instructions above")
    
    print()
    print("=" * 80)
    print("🎉 READY TO TEST REAL MARKET TRENDS DATA!")
    print("=" * 80)

if __name__ == "__main__":
    main()
