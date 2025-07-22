import requests
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import feedparser
import re
import socket
from urllib.parse import urljoin
import time

logger = logging.getLogger(__name__)

class CybersecurityNewsService:
    """Service to fetch real cybersecurity news from external sources"""
    
    def __init__(self):
        self.sources = {
            'bleeping_computer': {
                'name': 'BleepingComputer',
                'rss_url': 'https://www.bleepingcomputer.com/feed/',
                'website': 'https://www.bleepingcomputer.com',
                'priority': 'high'
            },
            'hacker_news': {
                'name': 'The Hacker News',
                'rss_url': 'https://feeds.feedburner.com/TheHackersNews',
                'website': 'https://thehackernews.com',
                'priority': 'high'
            },
            'cybernews': {
                'name': 'CyberNews',
                'rss_url': 'https://cybernews.com/feed/',
                'website': 'https://cybernews.com',
                'priority': 'high'
            },
            'security_week': {
                'name': 'SecurityWeek',
                'rss_url': 'https://www.securityweek.com/feed/',
                'website': 'https://www.securityweek.com',
                'priority': 'medium'
            }
        }
        
        # Set up requests session with proper headers to avoid blocking
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache'
        })
          # Keywords that indicate MDO/email security relevance
        self.mdo_keywords = [
            'microsoft', 'office 365', 'defender', 'email security', 'phishing',
            'malware', 'ransomware', 'business email compromise', 'bec',
            'zero-day', 'threat protection', 'advanced persistent threat',
            'email threat', 'outlook', 'exchange', 'cloud security'
        ]
    
    def fetch_cybersecurity_news(self, max_articles=10):
        """Fetch latest cybersecurity news from all sources"""
        all_articles = []
        
        # Check only the fastest/most reliable sources first for better performance
        priority_sources = ['bleeping_computer', 'hacker_news', 'infosecurity_magazine']
        
        for source_id in priority_sources:
            if source_id in self.sources:
                source_config = self.sources[source_id]
                try:
                    articles = self._fetch_from_rss(source_config, max_per_source=4)
                    all_articles.extend(articles)
                    logger.info(f"Fetched {len(articles)} articles from {source_config['name']}")
                    
                    # If we have enough articles, stop fetching to save time
                    if len(all_articles) >= max_articles * 2:
                        break
                        
                except Exception as e:
                    logger.error(f"Failed to fetch from {source_config['name']}: {str(e)}")
                    continue
        
        # Sort by relevance and date
        sorted_articles = sorted(all_articles, key=lambda x: (x['relevance_score'], x['published_date']), reverse=True)
          return sorted_articles[:max_articles]
    
    def _fetch_from_rss(self, source_config, max_per_source=3):
        """Fetch articles from RSS feed with improved error handling"""
        articles = []
        
        try:
            logger.info(f"Fetching from {source_config['name']}: {source_config['rss_url']}")
            
            # Use requests session with timeout instead of feedparser socket timeout
            response = self.session.get(
                source_config['rss_url'], 
                timeout=10,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Parse the RSS content
            feed = feedparser.parse(response.content)
            
            if not feed.entries:
                logger.warning(f"No entries found in feed for {source_config['name']}")
                return articles
            
            logger.info(f"Found {len(feed.entries)} entries in {source_config['name']} feed")
            
            for entry in feed.entries[:max_per_source * 3]:  # Get extra to filter
                try:
                    # Extract article data
                    title = getattr(entry, 'title', 'No Title')
                    link = getattr(entry, 'link', '')
                    summary = getattr(entry, 'summary', getattr(entry, 'description', ''))
                    published = getattr(entry, 'published_parsed', None)
                    
                    if not title or not link:
                        continue
                    
                    if published:
                        try:
                            published_date = datetime(*published[:6])
                        except (ValueError, TypeError):
                            published_date = datetime.now()
                    else:
                        published_date = datetime.now()
                    
                    # Only include recent articles (last 7 days)
                    if published_date < datetime.now() - timedelta(days=7):
                        continue
                    
                    # Calculate relevance score
                    relevance_score = self._calculate_relevance(title, summary)
                    
                    # Only include relevant articles (lowered threshold for testing)
                    if relevance_score >= 1.5:
                        article = {
                            'title': title,
                            'url': link,
                            'summary': self._clean_summary(summary)[:200] + '...',
                            'source': source_config['name'],
                            'published_date': published_date.isoformat(),
                            'relevance_score': relevance_score,
                            'priority': self._determine_priority(title, summary),
                            'category': self._categorize_article(title, summary),
                            'mdo_relevant': relevance_score >= 3.0
                        }
                        articles.append(article)
                        
                        if len(articles) >= max_per_source:
                            break
                        
                except Exception as e:
                    logger.error(f"Error processing article from {source_config['name']}: {str(e)}")
                    continue
            
            logger.info(f"Successfully processed {len(articles)} articles from {source_config['name']}")
            
        except requests.RequestException as e:
            logger.error(f"Network error fetching RSS from {source_config['name']}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching RSS from {source_config['name']}: {str(e)}")
        
        return articles
    
    def _calculate_relevance(self, title, summary):
        """Calculate relevance score based on MDO/email security keywords"""
        text = f"{title} {summary}".lower()
        score = 0
        
        # Base score for cybersecurity content
        score += 1
        
        # Bonus for MDO-specific keywords
        for keyword in self.mdo_keywords:
            if keyword in text:
                if keyword in ['microsoft', 'defender', 'office 365']:
                    score += 3  # High relevance
                elif keyword in ['email security', 'phishing', 'malware']:
                    score += 2  # Medium relevance
                else:
                    score += 1  # Low relevance
        
        return min(score, 10)  # Cap at 10
    
    def _determine_priority(self, title, summary):
        """Determine article priority based on content"""
        text = f"{title} {summary}".lower()
        
        critical_keywords = ['zero-day', 'breach', 'ransomware', 'critical vulnerability']
        high_keywords = ['malware', 'phishing', 'threat', 'attack']
        
        for keyword in critical_keywords:
            if keyword in text:
                return 'critical'
        
        for keyword in high_keywords:
            if keyword in text:
                return 'high'
        
        return 'medium'
    
    def _categorize_article(self, title, summary):
        """Categorize the article type"""
        text = f"{title} {summary}".lower()
        
        if any(word in text for word in ['vulnerability', 'cve', 'patch']):
            return 'vulnerability'
        elif any(word in text for word in ['malware', 'ransomware', 'trojan']):
            return 'malware'
        elif any(word in text for word in ['phishing', 'scam', 'social engineering']):
            return 'phishing'
        elif any(word in text for word in ['breach', 'hack', 'compromise']):
            return 'breach'
        elif any(word in text for word in ['policy', 'regulation', 'compliance']):
            return 'policy'
        else:
            return 'general'
    
    def _clean_summary(self, summary):
        """Clean HTML and format summary"""
        if not summary:
            return "Latest cybersecurity intelligence and threat analysis."
        
        # Remove HTML tags
        clean_summary = re.sub('<[^<]+?>', '', summary)
        
        # Remove extra whitespace
        clean_summary = ' '.join(clean_summary.split())
        
        return clean_summary
    
    def get_mdo_specific_news(self, max_articles=5):
        """Get news specifically relevant to MDO and email security"""
        all_news = self.fetch_cybersecurity_news(max_articles=20)
        
        # Filter for MDO-relevant articles
        mdo_news = [article for article in all_news if article['mdo_relevant']]
        
        return mdo_news[:max_articles]
