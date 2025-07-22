#!/usr/bin/env python3
"""
Simple test to check if reviews are being fetched correctly
"""

import os
import sys
import django
from pathlib import Path
import json

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'research_agent_backend.settings')
django.setup()

from research_agent.cybersecurity_news_service_new import CybersecurityNewsService
from research_agent.real_customer_reviews_service import RealCustomerReviewsService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    print("Testing review fetching...")
    
    # Test 1: Check if Reddit API is configured
    print("\n1. Checking Reddit API configuration...")
    from dotenv import load_dotenv
    load_dotenv()
    
    reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
    reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    
    if reddit_client_id and reddit_client_secret:
        print(f"✅ Reddit API configured (Client ID: {reddit_client_id[:10]}...)")
    else:
        print("❌ Reddit API not configured")
        return
    
    # Test 2: Initialize services
    print("\n2. Initializing services...")
    try:
        real_reviews_service = RealCustomerReviewsService()
        news_service = CybersecurityNewsService()
        print("✅ Services initialized")
    except Exception as e:
        print(f"❌ Error initializing services: {e}")
        return
    
    # Test 3: Test Reddit connection
    print("\n3. Testing Reddit connection...")
    try:
        if real_reviews_service.reddit:
            # Test authentication
            test_subreddit = real_reviews_service.reddit.subreddit('test')
            test_subreddit.id
            print("✅ Reddit authentication successful")
        else:
            print("❌ Reddit client not initialized")
    except Exception as e:
        print(f"❌ Reddit authentication failed: {e}")
        return
    
    # Test 4: Fetch reviews for Microsoft Defender
    print("\n4. Fetching reviews for Microsoft Defender for Office 365...")
    try:
        product_name = "Microsoft Defender for Office 365"
        reviews = news_service.fetch_real_customer_reviews(product_name, max_reviews=3)
        
        if reviews:
            print(f"✅ Fetched {len(reviews)} reviews")
            
            # Display each review
            for i, review in enumerate(reviews):
                print(f"\n📝 Review {i+1}:")
                print(f"   Platform: {review.get('platform', 'Unknown')}")
                print(f"   Rating: {review.get('rating', 'N/A')}")
                print(f"   Verified: {review.get('verified', False)}")
                print(f"   Content Type: {review.get('content_type', 'Unknown')}")
                print(f"   Text: {review.get('review_text', 'No text')[:100]}...")
                
                if review.get('content_type') == 'system_notice':
                    print("   ⚠️  This is a system notice")
                elif review.get('verified', False):
                    print("   ✅ This is a verified customer review")
        else:
            print("❌ No reviews fetched")
    except Exception as e:
        print(f"❌ Error fetching reviews: {e}")
        return
    
    # Test 5: Test the API endpoint data structure
    print("\n5. Testing API endpoint data structure...")
    try:
        from research_agent.views import product_intelligence
        from django.http import HttpRequest
        
        request = HttpRequest()
        request.method = 'GET'
        
        response = product_intelligence(request)
        
        if response.status_code == 200:
            data = json.loads(response.content)
            
            print("✅ API endpoint working")
            print(f"   Response keys: {list(data.keys())}")
            
            # Check if customer sentiment exists
            customer_sentiment = data.get('customer_sentiment', {})
            real_reviews = customer_sentiment.get('real_customer_reviews', [])
            
            print(f"   Customer reviews in response: {len(real_reviews)}")
            
            if real_reviews:
                print("   Review breakdown:")
                for i, review in enumerate(real_reviews[:3]):
                    print(f"     {i+1}. {review.get('platform', 'Unknown')} - {review.get('content_type', 'Unknown')}")
            else:
                print("   ❌ No customer reviews in API response")
                
        else:
            print(f"❌ API endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API endpoint error: {e}")
    
    print("\n🎯 Test complete!")

if __name__ == "__main__":
    main()
