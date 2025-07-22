#!/usr/bin/env python
"""
Server status checker and URL opener
"""
import requests
import time
import webbrowser

def check_servers():
    print("🔍 Checking server status...")
    
    # Check Django backend
    try:
        backend_response = requests.get('http://127.0.0.1:3000/research-agent/real-market-trends-data/', timeout=5)
        if backend_response.status_code == 200:
            print("✅ Django backend is running!")
            data = backend_response.json()
            print(f"   📊 Sample data: Market Size = {data.get('market_size_2025', {}).get('value', 'N/A')}")
        else:
            print(f"⚠️ Django backend responded with status: {backend_response.status_code}")
    except Exception as e:
        print(f"❌ Django backend not accessible: {e}")
        print("   📋 Make sure to run: python manage.py runserver 3000")
        return False
    
    # Check React frontend  
    try:
        frontend_response = requests.get('http://localhost:5173', timeout=5)
        if frontend_response.status_code == 200:
            print("✅ React frontend is running!")
        else:
            print(f"⚠️ React frontend responded with status: {frontend_response.status_code}")
    except Exception as e:
        print(f"❌ React frontend not accessible: {e}")
        print("   📋 Make sure to run: npm run dev")
        return False
    
    return True

def main():
    print("🌐 Server Status Checker")
    print("=" * 40)
    
    if check_servers():
        print("\n🎉 Both servers are running!")
        print("🌐 Opening browser to show real market trends data...")
        
        # Open the Market Trends page
        webbrowser.open('http://localhost:5173')
        
        print("\n📊 Navigate to 'Market Trends' to see:")
        print("   ✅ Real market size calculations")
        print("   ✅ Real MDO market share data")
        print("   ✅ Real threat volume metrics")
        print("   ✅ Real AI adoption rates")
        print("   ✅ Data source transparency")
    else:
        print("\n⚠️ Servers not fully ready yet")
        print("⏳ Please wait and try again in a few seconds")

if __name__ == "__main__":
    main()
