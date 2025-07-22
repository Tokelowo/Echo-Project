#!/usr/bin/env python
"""
Quick connection test for the Django backend and React frontend.
This script will test the API endpoints and provide connection diagnostics.
"""

import requests
import json
import sys
import time
from urllib.parse import urljoin

# Configuration
DJANGO_BASE_URL = "http://127.0.0.1:8000"
REACT_PORTS = [3000, 3001, 3002, 3003, 3004, 3005]

def test_django_connection():
    """Test if Django backend is running and accessible."""
    print("🔍 Testing Django Backend Connection...")
    print(f"Backend URL: {DJANGO_BASE_URL}")
    
    # Test endpoints that should exist
    endpoints_to_test = [
        "/research-agent/overview/",
        "/research-agent/competitive-metrics/",
        "/research-agent/customer-reviews/",
        "/research-agent/market-intelligence/"
    ]
    
    results = []
    
    for endpoint in endpoints_to_test:
        url = urljoin(DJANGO_BASE_URL, endpoint)
        try:
            print(f"  Testing: {url}")
            response = requests.get(url, timeout=10, params={'force_refresh': 'false'})
            
            if response.status_code == 200:
                print(f"    ✅ SUCCESS: {response.status_code}")
                try:
                    data = response.json()
                    print(f"    📊 Response has {len(data)} keys" if isinstance(data, dict) else f"    📊 Response type: {type(data)}")
                except:
                    print(f"    📄 Non-JSON response: {len(response.text)} characters")
            else:
                print(f"    ❌ FAILED: {response.status_code} - {response.reason}")
                
            results.append({
                'endpoint': endpoint,
                'status_code': response.status_code,
                'success': response.status_code == 200
            })
            
        except requests.ConnectionError as e:
            print(f"    🚫 CONNECTION ERROR: {str(e)}")
            results.append({
                'endpoint': endpoint,
                'error': 'Connection refused - Django server not running?',
                'success': False
            })
        except requests.Timeout as e:
            print(f"    ⏰ TIMEOUT ERROR: {str(e)}")
            results.append({
                'endpoint': endpoint,
                'error': 'Request timeout',
                'success': False
            })
        except Exception as e:
            print(f"    ❌ ERROR: {str(e)}")
            results.append({
                'endpoint': endpoint,
                'error': str(e),
                'success': False
            })
    
    return results

def check_react_ports():
    """Check which React development ports are active."""
    print("\n🔍 Checking React Development Ports...")
    
    active_ports = []
    
    for port in REACT_PORTS:
        try:
            url = f"http://127.0.0.1:{port}"
            print(f"  Testing: {url}")
            response = requests.get(url, timeout=3)
            
            if response.status_code == 200:
                print(f"    ✅ ACTIVE: Port {port}")
                active_ports.append(port)
            else:
                print(f"    ⚠️  Port {port}: {response.status_code}")
                
        except requests.ConnectionError:
            print(f"    🚫 Port {port}: Not active")
        except requests.Timeout:
            print(f"    ⏰ Port {port}: Timeout")
        except Exception as e:
            print(f"    ❌ Port {port}: {str(e)}")
    
    return active_ports

def provide_recommendations(django_results, active_react_ports):
    """Provide recommendations based on test results."""
    print("\n📋 DIAGNOSIS AND RECOMMENDATIONS")
    print("=" * 50)
    
    # Check Django status
    django_working = any(result.get('success', False) for result in django_results)
    
    if not django_working:
        print("🚨 DJANGO BACKEND ISSUE DETECTED:")
        print("   The Django backend server appears to be down or not accessible.")
        print("   This explains the 'Failed to fetch' errors in your React app.")
        print("\n💡 SOLUTION:")
        print("   1. Start the Django backend server:")
        print("      cd c:\\Users\\t-tokelowo\\OneDrive - Microsoft\\Agent 1\\django-backend")
        print("      python manage.py runserver 8000")
        print("   2. Or use the start script:")
        print("      python start_django_server.py")
        
    else:
        print("✅ DJANGO BACKEND: Working properly")
        
        # Check specific failing endpoints
        failed_endpoints = [r for r in django_results if not r.get('success', False)]
        if failed_endpoints:
            print("⚠️  Some endpoints are having issues:")
            for result in failed_endpoints:
                print(f"   - {result['endpoint']}: {result.get('error', 'Unknown error')}")
    
    # Check React status
    if active_react_ports:
        print(f"\n✅ REACT FRONTEND: Active on port(s) {active_react_ports}")
        print("   Your React app should be able to connect once Django is running.")
    else:
        print("\n🚨 REACT FRONTEND: No active development servers detected")
        print("💡 SOLUTION:")
        print("   1. Start your React development server:")
        print("      cd c:\\Users\\t-tokelowo\\OneDrive - Microsoft\\Attachments\\React")
        print("      npm run dev")
        print("   2. Make sure it runs on a port between 3000-3005")
    
    # CORS configuration check
    print(f"\n🔧 CORS CONFIGURATION: Updated to support ports 3000-3005")
    print("   The Django CORS settings have been updated to allow:")
    for port in REACT_PORTS:
        print(f"   - http://localhost:{port} and http://127.0.0.1:{port}")

def main():
    """Main function to run all connection tests."""
    print("🚀 FRONTEND-BACKEND CONNECTION DIAGNOSTICS")
    print("=" * 60)
    print("This tool will help diagnose the 'Failed to fetch' errors")
    print("you're experiencing in your React frontend.\n")
    
    # Test Django backend
    django_results = test_django_connection()
    
    # Check React ports
    active_react_ports = check_react_ports()
    
    # Provide recommendations
    provide_recommendations(django_results, active_react_ports)
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY:")
    print("   - Django Backend configured for port 8000")
    print("   - React Frontend configured for ports 3000-3005") 
    print("   - CORS settings updated to allow cross-origin requests")
    print("   - API base URL updated from port 3000 to 8000")
    
    # Final status
    django_working = any(result.get('success', False) for result in django_results)
    if django_working and active_react_ports:
        print("\n🎉 STATUS: Ready for frontend-backend communication!")
    elif django_working:
        print("\n⚠️  STATUS: Backend ready, start React frontend")
    elif active_react_ports:
        print("\n⚠️  STATUS: Frontend ready, start Django backend")
    else:
        print("\n🚨 STATUS: Both frontend and backend need to be started")

if __name__ == "__main__":
    main()
