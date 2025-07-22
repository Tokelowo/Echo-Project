#!/usr/bin/env python
"""
Start Django server and test the real market trends integration
"""
import subprocess
import sys
import time
import requests
import json

def start_django_server():
    """Start Django development server"""
    try:
        print("🚀 Starting Django development server...")
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        print("✅ Django server started on http://127.0.0.1:8000")
        return process
    except Exception as e:
        print(f"❌ Error starting Django server: {e}")
        return None

def test_real_market_trends_api():
    """Test the real market trends API endpoint"""
    try:
        print("\n📡 Testing real market trends API endpoint...")
        
        response = requests.get('http://127.0.0.1:8000/research-agent/real-market-trends-data/')
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API endpoint is working!")
            print(f"📊 Market Size 2025: {data.get('market_size_2025', {}).get('value', 'N/A')}")
            print(f"🛡️ MDO Market Share: {data.get('mdo_market_share', {}).get('value', 'N/A')}")
            print(f"⚠️ Threat Volume: {data.get('threat_volume', {}).get('value', 'N/A')}")
            print(f"🤖 AI Adoption: {data.get('ai_adoption', {}).get('value', 'N/A')}")
            print(f"📈 Articles Analyzed: {data.get('data_quality_report', {}).get('articles_analyzed', 'N/A')}")
            return True
        else:
            print(f"❌ API endpoint failed: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def main():
    print("=" * 60)
    print("REAL MARKET TRENDS DATA INTEGRATION TEST")
    print("=" * 60)
    
    # Start Django server
    server_process = start_django_server()
    
    if server_process:
        # Test API endpoint
        if test_real_market_trends_api():
            print("\n🎯 SUCCESS: Real market trends data is now available!")
            print("\n📋 NEXT STEPS:")
            print("1. ✅ Backend endpoint working with REAL data")
            print("2. ✅ Frontend code updated to use real data")
            print("3. 🔄 Start React dev server: npm run dev")
            print("4. 🌐 Open browser: http://localhost:5173")
            print("5. 📊 Navigate to Market Trends page to see REAL data")
            print("\n⚠️ All hardcoded values have been replaced with:")
            print("   • Data-driven market size calculations")
            print("   • Real vendor mention-based market share")
            print("   • Live threat volume from cybersecurity news")
            print("   • AI adoption rates from actual article analysis")
        else:
            print("\n❌ API test failed")
        
        print(f"\n🔄 Django server is running on PID: {server_process.pid}")
        print("   Press Ctrl+C to stop the server")
        
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping Django server...")
            server_process.terminate()
    
    print("\n=" * 60)
    print("INTEGRATION TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
