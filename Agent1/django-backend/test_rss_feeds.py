#!/usr/bin/env python
"""
Test RSS feeds directly to diagnose 403 errors
"""
import requests
import feedparser
from datetime import datetime

def test_rss_feeds():
    """Test each RSS feed individually"""
    
    feeds = {
        'BleepingComputer': 'https://www.bleepingcomputer.com/feed/',
        'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
        'CyberNews': 'https://cybernews.com/feed/',
        'SecurityWeek': 'https://www.securityweek.com/feed/'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    print("🔍 Testing RSS feeds for 403 errors...")
    
    for name, url in feeds.items():
        print(f"\n📡 Testing {name}: {url}")
        try:
            response = session.get(url, timeout=10, allow_redirects=True)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                # Try parsing with feedparser
                feed = feedparser.parse(response.content)
                entries_count = len(feed.entries)
                print(f"   ✅ SUCCESS: {entries_count} articles found")
                
                if entries_count > 0:
                    first_article = feed.entries[0]
                    print(f"   📰 Sample: {first_article.title[:60]}...")
                
            elif response.status_code == 403:
                print(f"   ❌ 403 FORBIDDEN - Site is blocking requests")
            else:
                print(f"   ⚠️  HTTP {response.status_code}: {response.reason}")
                
        except requests.RequestException as e:
            print(f"   💥 REQUEST ERROR: {str(e)}")
        except Exception as e:
            print(f"   💥 PARSING ERROR: {str(e)}")

if __name__ == "__main__":
    test_rss_feeds()
