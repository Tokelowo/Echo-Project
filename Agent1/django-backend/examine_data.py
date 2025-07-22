#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.cybersecurity_news_service_new import CybersecurityNewsService

def examine_real_data():
    news_service = CybersecurityNewsService()
    
    # Fetch real data
    print("Fetching cybersecurity articles...")
    articles = news_service.fetch_cybersecurity_news(max_articles=15)
    
    print(f"\n=== FETCHED {len(articles)} ARTICLES ===")
    
    if articles:
        print("\nSample article structure:")
        sample = articles[0]
        for key, value in sample.items():
            print(f"  {key}: {str(value)[:100]}...")
    
    # Analyze data
    print("\n=== ANALYZING DATA ===")
    market_presence = news_service.analyze_market_presence(articles)
    tech_trends = news_service.analyze_technology_trends(articles)
    competitive_landscape = news_service.analyze_competitive_landscape(articles)
    threat_landscape = news_service.analyze_threat_landscape(articles)
    
    print('\n=== MARKET PRESENCE DATA ===')
    for vendor, data in market_presence.items():
        print(f'{vendor}: {data}')
    
    print('\n=== TECHNOLOGY TRENDS ===')
    for tech, count in tech_trends.items():
        if count > 0:
            print(f'{tech}: {count} mentions')
    
    print('\n=== COMPETITIVE LANDSCAPE ===') 
    for competitor, data in competitive_landscape.items():
        if isinstance(data, dict) and data.get('articles_count', 0) > 0:
            print(f'{competitor}: {data}')
    
    print('\n=== THREAT LANDSCAPE ===')
    for threat, data in threat_landscape.items():
        if isinstance(data, dict) and data.get('articles_count', 0) > 0:
            print(f'{threat}: {data}')
        elif isinstance(data, (int, float)) and data > 0:
            print(f'{threat}: {data}')

if __name__ == "__main__":
    examine_real_data()
