#!/usr/bin/env python3
"""
Complete System Verification Script
Tests all functionality after security enhancement implementation
"""

import requests
import json
import time
from datetime import datetime

def test_endpoint(url, method="GET", data=None, description="", api_key=None):
    """Test an API endpoint and return results"""
    try:
        headers = {'Content-Type': 'application/json'}
        
        # Add API key if provided
        if api_key:
            headers['X-API-Key'] = api_key
            
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        
        result = {
            'url': url,
            'method': method,
            'status_code': response.status_code,
            'description': description,
            'success': response.status_code == 200,
            'headers': dict(response.headers),
            'content_length': len(response.content)
        }
        
        if response.status_code == 200:
            try:
                result['json_response'] = response.json()
            except:
                result['text_response'] = response.text[:200] + "..." if len(response.text) > 200 else response.text
        
        return result
        
    except Exception as e:
        return {
            'url': url,
            'method': method,
            'status_code': 'ERROR',
            'description': description,
            'success': False,
            'error': str(e)
        }

def check_security_headers(headers):
    """Check if required security headers are present"""
    security_headers = {
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }
    
    results = {}
    for header, expected in security_headers.items():
        if header in headers:
            results[header] = {
                'present': True,
                'value': headers[header],
                'matches_expected': headers[header] == expected
            }
        else:
            results[header] = {'present': False, 'value': None, 'matches_expected': False}
    
    return results

def main():
    """Run comprehensive system verification"""
    print("🔍 COMPREHENSIVE SYSTEM VERIFICATION")
    print("=" * 50)
    print(f"Testing Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Base URL and API key
    base_url = "http://localhost:8000"
    api_key = "mdo-security-2024-enhanced-api-key-f8e9d0a1b2c3d4e5f6789xyz"
    
    # Test endpoints
    endpoints_to_test = [
        (f"{base_url}/", "GET", None, "Root Dashboard Endpoint", None),
        (f"{base_url}/api/research/", "GET", None, "Research API Endpoint", api_key),
        (f"{base_url}/api/market-trends/", "GET", None, "Market Trends API", None),
        (f"{base_url}/api/competitive-intelligence/", "GET", None, "Competitive Intelligence API", None),
        (f"{base_url}/api/product-intelligence/", "GET", None, "Product Intelligence API", None),
        (f"{base_url}/api/admin/", "GET", None, "Admin API Endpoint", api_key),
    ]
    
    results = []
    all_passed = True
    
    print("🌐 TESTING API ENDPOINTS")
    print("-" * 25)
    
    for url, method, data, description, auth_key in endpoints_to_test:
        print(f"Testing: {description}")
        result = test_endpoint(url, method, data, description, auth_key)
        results.append(result)
        
        if result['success']:
            print(f"✅ {description}: Status {result['status_code']}")
            if 'json_response' in result:
                if 'message' in result['json_response']:
                    print(f"   📝 Message: {result['json_response']['message']}")
        else:
            print(f"❌ {description}: Status {result['status_code']}")
            if 'error' in result:
                print(f"   🚨 Error: {result['error']}")
            all_passed = False
        
        print()
    
    print("🔐 SECURITY HEADERS VERIFICATION")
    print("-" * 32)
    
    # Check security headers on one endpoint
    test_result = next((r for r in results if r['success']), None)
    if test_result:
        security_check = check_security_headers(test_result['headers'])
        
        for header, info in security_check.items():
            if info['present']:
                status = "✅" if info['matches_expected'] else "⚠️"
                print(f"{status} {header}: {info['value']}")
            else:
                print(f"❌ {header}: MISSING")
                all_passed = False
    
    print()
    print("📊 SUMMARY REPORT")
    print("-" * 16)
    
    passed_tests = sum(1 for r in results if r['success'])
    total_tests = len(results)
    
    print(f"✅ Passed: {passed_tests}/{total_tests} endpoints")
    print(f"🔐 Security Headers: {'ACTIVE' if test_result else 'UNKNOWN'}")
    print(f"🚀 Overall Status: {'SYSTEM OPERATIONAL' if all_passed else 'ISSUES DETECTED'}")
    
    if all_passed:
        print("\n🎉 VERIFICATION COMPLETE: All systems operational!")
        print("   - All API endpoints responding correctly")
        print("   - Security middleware functioning properly")
        print("   - No blocking issues detected")
        print("   - Ready for production use")
    else:
        print("\n⚠️  VERIFICATION ISSUES: Some problems detected")
        print("   - Review failed tests above")
        print("   - Address issues before production")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
