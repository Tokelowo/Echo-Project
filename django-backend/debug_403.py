#!/usr/bin/env python3
"""
Quick diagnostic test to see what's causing 403 errors
"""

import requests
import json

def test_with_details():
    """Test endpoint with detailed error reporting"""
    url = "http://localhost:8000/"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content: {response.text}")
        
        # Test with API key
        print("\n" + "="*50)
        print("Testing with API key:")
        
        headers = {'X-API-Key': 'mdo-security-2024-enhanced-api-key-f8e9d0a1b2c3d4e5f6789xyz'}
        response2 = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response2.status_code}")
        print(f"Headers: {dict(response2.headers)}")
        print(f"Content: {response2.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_with_details()
