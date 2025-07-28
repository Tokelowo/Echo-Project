#!/usr/bin/env python
"""
Test the email generation with fixed metrics
"""
import os
import sys
import django
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.cybersecurity_news_service_new import CybersecurityNewsService
from research_agent.enhanced_email_service import EnhancedEmailService
from django.utils import timezone

def test_email_with_metrics():
    """Test email generation with the fixed metrics"""
    
    print("🧪 Testing email generation with fixed metrics...")
    
    try:
        # Generate news data
        news_service = CybersecurityNewsService()
        articles = news_service.fetch_cybersecurity_news(max_articles=20)
        
        print(f"📰 Fetched {len(articles)} articles")
        
        # Create featured articles
        featured_articles = []
        for i, article in enumerate(articles[:5]):
            featured_articles.append({
                'id': i + 1,
                'title': article.get('title', 'Cybersecurity Alert'),
                'summary': article.get('summary', 'No summary available'),
                'url': article.get('url', '#'),
                'source': article.get('source', 'Security News'),
                'published_date': article.get('published_date', timezone.now().isoformat()),
                'relevance_score': article.get('relevance_score', 5),
                'category': article.get('category', 'cybersecurity')
            })
        
        # Extract threat categories and competitors from articles
        threat_categories = set()
        competitors = set()
        
        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
            if 'phishing' in content: threat_categories.add('Phishing')
            if 'malware' in content: threat_categories.add('Malware')
            if 'ransomware' in content: threat_categories.add('Ransomware')
            if 'breach' in content or 'data breach' in content: threat_categories.add('Data Breach')
            if 'vulnerability' in content: threat_categories.add('Vulnerability')
            
            if 'proofpoint' in content: competitors.add('Proofpoint')
            if 'cisco' in content: competitors.add('Cisco')
            if 'symantec' in content: competitors.add('Symantec')
        
        # Create proper report data structure
        report_data = {
            'title': 'Test Comprehensive Multi-Agent Research Report',
            'summary': f'Test analysis of {len(articles)} real articles from live sources.',
            'articles': featured_articles,
            'microsoft_articles': [],
            'reddit_reviews': [],
            'articles_analyzed': len(articles),  # KEY METRIC
            'threat_analysis': list(threat_categories),  # KEY METRIC
            'competitive_analysis': list(competitors),  # KEY METRIC
            'market_intelligence': {  # KEY FIX: Add market intelligence structure
                'articles_analyzed': len(articles),
                'data_collection_timestamp': timezone.now().isoformat(),
                'real_market_indicators': {
                    'growth_keyword_mentions': 5,
                    'investment_mentions': 3,
                    'market_expansion_mentions': 2,
                    'growth_sentiment_score': 75
                },
                'real_competitive_landscape': {
                    'microsoft_mention_share': 12
                },
                'real_technology_adoption': {
                    'ai_ml_mentions': 8,
                    'zero_trust_mentions': 4,
                    'cloud_security_mentions': 12
                }
            },
            'metadata': {
                'generated_at': timezone.now().isoformat(),
                'real_data': True
            }
        }
        
        print(f"📊 Metrics calculated:")
        print(f"   Articles Analyzed: {report_data['articles_analyzed']}")
        print(f"   Threat Categories: {len(report_data['threat_analysis'])}")
        print(f"   Competitors Tracked: {len(report_data['competitive_analysis'])}")
        
        # Test email generation
        email_service = EnhancedEmailService()
        result = email_service.send_professional_report_email(
            report_data, 
            "t-tokelowo@microsoft.com",
            "Temiloluwa Okelowo"
        )
        
        print(f"✅ Email result: {result.get('status')}")
        print(f"📧 Message: {result.get('message')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_email_with_metrics()
