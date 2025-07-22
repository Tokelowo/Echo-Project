"""
Demo Customer Reviews Fallback Service
Provides realistic demo data when external APIs are unavailable
"""

from datetime import datetime, timedelta
import random
from typing import List, Dict

class DemoCustomerReviewsService:
    """Provides realistic demo customer review data when APIs are unavailable"""
    
    def __init__(self):
        self.demo_reviews = {
            'Microsoft Defender for Office 365': [
                {
                    'platform': 'Demo - G2 Style',
                    'product': 'Microsoft Defender for Office 365',
                    'rating': 4,
                    'review_text': 'We deployed MDO across our organization last year. The phishing protection has been excellent - caught several sophisticated attacks that our previous solution missed. Integration with Office 365 is seamless. Setup took about 2 weeks but support was helpful throughout.',
                    'reviewer': 'IT Director - Healthcare',
                    'source_url': '#demo-review-1',
                    'date_scraped': (datetime.now() - timedelta(days=15)).isoformat(),
                    'content_type': 'demo_professional_review',
                    'verified': False,
                    'is_demo': True
                },
                {
                    'platform': 'Demo - TrustRadius Style',
                    'product': 'Microsoft Defender for Office 365',
                    'rating': 5,
                    'review_text': 'Been using Defender for Office 365 for 18 months now. The SafeAttachments feature has been a game-changer for our company. We had a zero-day malware attempt last month and it was blocked immediately. The reporting dashboard gives our team great visibility.',
                    'reviewer': 'Security Administrator',
                    'source_url': '#demo-review-2',
                    'date_scraped': (datetime.now() - timedelta(days=8)).isoformat(),
                    'content_type': 'demo_professional_review',
                    'verified': False,
                    'is_demo': True
                },
                {
                    'platform': 'Demo - Reddit Style',
                    'product': 'Microsoft Defender for Office 365',
                    'rating': 3,
                    'review_text': 'Our experience with MDO has been mixed. The advanced threat protection works well, but we had some issues with false positives in the first few months. Support helped us tune the policies and its much better now. Worth it for the Microsoft 365 integration.',
                    'reviewer': 'u/sysadmin_pro',
                    'source_url': '#demo-review-3',
                    'date_scraped': (datetime.now() - timedelta(days=22)).isoformat(),
                    'content_type': 'demo_reddit_discussion',
                    'verified': False,
                    'is_demo': True
                }
            ]
        }
    
    def get_demo_reviews(self, product_name: str, max_reviews: int = 10) -> List[Dict]:
        """Get demo customer reviews with clear indicators they are not real"""
        
        reviews = self.demo_reviews.get(product_name, [])
        
        # Add system notice about demo data
        demo_notice = {
            'platform': 'SYSTEM NOTICE',
            'product': product_name,
            'rating': 0,
            'review_text': '⚠️ DEMO MODE: External review APIs (Reddit, G2, TrustRadius) are currently unavailable due to authentication issues. The reviews shown below are realistic examples for demonstration purposes only. Configure API keys in .env to see real customer reviews.',
            'reviewer': 'System Administrator',
            'source_url': '#api-configuration-needed',
            'date_scraped': datetime.now().isoformat(),
            'content_type': 'system_notice',
            'verified': False,
            'is_demo': True
        }
        
        # Return notice plus demo reviews
        result = [demo_notice] + reviews[:max_reviews-1]
        
        return result
    
    def get_review_statistics(self, reviews: List[Dict]) -> Dict:
        """Generate statistics for demo reviews"""
        if not reviews:
            return {}
        
        # Filter out system notices for stats
        real_reviews = [r for r in reviews if r.get('content_type') != 'system_notice']
        
        if not real_reviews:
            return {}
        
        total_reviews = len(real_reviews)
        avg_rating = sum(r.get('rating', 0) for r in real_reviews) / total_reviews
        
        return {
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2),
            'platform_distribution': {'Demo Platforms': total_reviews},
            'rating_distribution': {i: sum(1 for r in real_reviews if r.get('rating') == i) for i in range(1, 6)},
            'latest_review_date': max(r.get('date_scraped', '') for r in real_reviews),
            'data_freshness': 'demo-data',
            'authenticity': 'demo_data_api_unavailable'
        }
