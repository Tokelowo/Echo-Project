"""
Debug Customer Reviews in API
"""
import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.cybersecurity_news_service_new import CybersecurityNewsService

def debug_customer_reviews():
    """Debug why customer reviews aren't showing in API"""
    print("Debugging customer reviews flow...")
    
    service = CybersecurityNewsService()
    
    print("1. Testing fetch_real_customer_reviews method...")
    reviews = service.fetch_real_customer_reviews('Microsoft Defender for Office 365', max_reviews=5)
    
    print(f"2. Direct service call returned: {len(reviews)} reviews")
    
    if reviews:
        for i, review in enumerate(reviews[:2], 1):
            print(f"Review {i}:")
            print(f"  Platform: {review.get('platform')}")
            print(f"  Content Type: {review.get('content_type')}")
            print(f"  Verified: {review.get('verified')}")
            print(f"  Authenticity: {review.get('authenticity', 'N/A')}")
            print(f"  Text: {review.get('review_text', '')[:100]}...")
    else:
        print("❌ No reviews returned from main service")
        
    print("\n3. Testing individual review services...")
    
    # Test Reddit service directly
    reddit_reviews = service.real_reviews_service.fetch_reddit_discussions('Microsoft Defender for Office 365', max_reviews=3)
    print(f"Reddit service returned: {len(reddit_reviews)} reviews")
    
    # Test enhanced service
    enhanced_reviews = service.enhanced_reviews_service.fetch_daily_reviews('Microsoft Defender for Office 365', max_reviews=3)
    print(f"Enhanced service returned: {len(enhanced_reviews)} reviews")

if __name__ == "__main__":
    debug_customer_reviews()
