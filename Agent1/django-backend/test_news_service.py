#!/usr/bin/env python
"""
Test the fixed cybersecurity news service
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.cybersecurity_news_service_new import CybersecurityNewsService

def test_news_service():
    """Test the cybersecurity news service"""
    
    print("🔍 Testing fixed cybersecurity news service...")
    
    service = CybersecurityNewsService()
    
    print("📡 Fetching cybersecurity news...")
    articles = service.fetch_cybersecurity_news(max_articles=10)
    
    print(f"✅ Found {len(articles)} articles")
    
    if articles:
        print("\n📰 Sample articles:")
        for i, article in enumerate(articles[:3], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   URL: {article['url']}")
            print(f"   Score: {article['relevance_score']}")
            print(f"   Summary: {article['summary'][:100]}...")
    else:
        print("❌ No articles found!")
    
    return len(articles) > 0

if __name__ == "__main__":
    success = test_news_service()
    if success:
        print("\n🎉 News service is working!")
    else:
        print("\n💥 News service failed!")
