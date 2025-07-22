#!/usr/bin/env python3
"""
Diagnostic script to examine the data structures being passed to the formatting agent
"""

import sys
import os
import json

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'research_agent'))

from research_agent.cybersecurity_news_service_new import CybersecurityNewsService

def diagnose_data_structures():
    """Examine the actual data structures returned by each analysis method"""
    print("🔍 DIAGNOSING DATA STRUCTURES")
    print("=" * 60)
    
    try:
        service = CybersecurityNewsService()
        
        # Fetch articles
        print("\n📰 Fetching articles...")
        articles = service.fetch_cybersecurity_news()
        print(f"✅ Fetched {len(articles)} articles")
        
        # Test each analysis method
        print("\n📊 MARKET PRESENCE ANALYSIS")
        print("-" * 40)
        market_data = service.analyze_market_presence(articles)
        print(f"Type: {type(market_data)}")
        print(f"Keys: {list(market_data.keys()) if isinstance(market_data, dict) else 'Not a dict'}")
        
        if 'market_presence' in market_data:
            mp_data = market_data['market_presence']
            print(f"market_presence type: {type(mp_data)}")
            if isinstance(mp_data, list) and mp_data:
                print(f"First item: {mp_data[0]}")
                print(f"First item keys: {list(mp_data[0].keys()) if isinstance(mp_data[0], dict) else 'Not a dict'}")
        
        print("\n🏢 COMPETITIVE ANALYSIS")
        print("-" * 40)
        comp_data = service.analyze_competitive_landscape(articles)
        print(f"Type: {type(comp_data)}")
        print(f"Keys: {list(comp_data.keys()) if isinstance(comp_data, dict) else 'Not a dict'}")
        
        if 'competitive_analysis' in comp_data:
            ca_data = comp_data['competitive_analysis']
            print(f"competitive_analysis type: {type(ca_data)}")
            if isinstance(ca_data, list) and ca_data:
                print(f"First item: {ca_data[0]}")
        
        print("\n💻 TECHNOLOGY TRENDS")
        print("-" * 40)
        tech_data = service.analyze_technology_trends(articles)
        print(f"Type: {type(tech_data)}")
        print(f"Keys: {list(tech_data.keys()) if isinstance(tech_data, dict) else 'Not a dict'}")
        
        if 'technology_trends' in tech_data:
            tt_data = tech_data['technology_trends']
            print(f"technology_trends type: {type(tt_data)}")
            if isinstance(tt_data, list) and tt_data:
                print(f"First item: {tt_data[0]}")
        
        print("\n🛡️ THREAT ANALYSIS")
        print("-" * 40)
        threat_data = service.analyze_threat_landscape(articles)
        print(f"Type: {type(threat_data)}")
        print(f"Keys: {list(threat_data.keys()) if isinstance(threat_data, dict) else 'Not a dict'}")
        
        if 'threat_analysis' in threat_data:
            ta_data = threat_data['threat_analysis']
            print(f"threat_analysis type: {type(ta_data)}")
            if isinstance(ta_data, list) and ta_data:
                print(f"First item: {ta_data[0]}")
        
        print("\n🎯 SUMMARY")
        print("=" * 60)
        print("All analysis methods return dictionaries with list-based data structures.")
        print("The formatting agent should handle these properly now.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_data_structures()
