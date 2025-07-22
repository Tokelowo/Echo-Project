"""
Web Scraping Service for News and Market Intelligence

This service aggregates information from WSJ, Reuters, TechCrunch, and other sources
to provide real-time data about Microsoft's products and competitors.
"""

import requests
from bs4 import BeautifulSoup
import feedparser
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
import time
import re
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)

@dataclass
class NewsArticle:
    """Data class for news articles"""
    title: str
    url: str
    content: str
    source: str
    published_date: Optional[datetime]
    author: Optional[str]
    summary: str
    relevance_score: float = 0.0

class WebScrapingService:
    """Service for scraping news and market intelligence from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Rate limiting
        self.request_delay = 1  # seconds between requests
        self.last_request_time = 0
        
        # News sources configuration
        self.news_sources = {
            'wsj': {
                'name': 'Wall Street Journal',
                'rss_feeds': [
                    'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
                    'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
                    'https://feeds.a.dj.com/rss/RSSWSJD.xml'  # WSJ Technology
                ],
                'search_base': 'https://www.wsj.com/search?query='
            },
            'reuters': {
                'name': 'Reuters',
                'rss_feeds': [
                    'https://www.reuters.com/rssFeed/technologyNews',
                    'https://www.reuters.com/rssFeed/businessNews'
                ]
            },
            'techcrunch': {
                'name': 'TechCrunch',
                'rss_feeds': [
                    'https://techcrunch.com/feed/'
                ]
            },
            'theregister': {
                'name': 'The Register',
                'rss_feeds': [
                    'https://www.theregister.com/headlines.atom'
                ]
            },
            'arstechnica': {
                'name': 'Ars Technica',
                'rss_feeds': [
                    'https://feeds.arstechnica.com/arstechnica/index'
                ]
            }
        }
        
        # Company keywords for filtering
        self.microsoft_keywords = [
            'microsoft', 'azure', 'office 365', 'teams', 'windows', 'xbox',
            'surface', 'dynamics', 'power platform', 'copilot', 'bing',
            'onedrive', 'sharepoint', 'outlook', 'visual studio'
        ]
        
        self.competitor_keywords = {
            'google': ['google', 'alphabet', 'gmail', 'chrome', 'android', 'youtube', 'google cloud', 'workspace'],
            'apple': ['apple', 'iphone', 'ipad', 'mac', 'ios', 'macos', 'app store', 'icloud'],
            'amazon': ['amazon', 'aws', 'alexa', 'prime', 'kindle', 'echo'],
            'meta': ['meta', 'facebook', 'instagram', 'whatsapp', 'oculus', 'metaverse'],
            'salesforce': ['salesforce', 'tableau', 'slack', 'trailhead'],
            'oracle': ['oracle', 'java', 'mysql', 'oracle cloud'],
            'ibm': ['ibm', 'watson', 'red hat', 'cloud pak'],
            'zoom': ['zoom', 'zoom meetings', 'zoom phone'],
            'dropbox': ['dropbox', 'dropbox business'],
            'slack': ['slack', 'slack technologies']
        }

    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        if current_time - self.last_request_time < self.request_delay:
            time.sleep(self.request_delay - (current_time - self.last_request_time))
        self.last_request_time = time.time()

    def _make_request(self, url: str, timeout: int = 10) -> Optional[requests.Response]:
        """Make a rate-limited HTTP request"""
        try:
            self._rate_limit()
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {str(e)}")
            return None

    def get_rss_articles(self, feed_url: str, max_articles: int = 20) -> List[NewsArticle]:
        """Get articles from RSS feed"""
        articles = []
        try:
            self._rate_limit()
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:max_articles]:
                try:
                    # Parse published date
                    published_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published_date = datetime(*entry.updated_parsed[:6])
                    
                    # Get content
                    content = ""
                    if hasattr(entry, 'content') and entry.content:
                        content = entry.content[0].value if entry.content else ""
                    elif hasattr(entry, 'description'):
                        content = entry.description
                    elif hasattr(entry, 'summary'):
                        content = entry.summary
                    
                    # Clean content
                    content = self._clean_html(content)
                    
                    article = NewsArticle(
                        title=entry.title,
                        url=entry.link,
                        content=content,
                        source=feed.feed.title if hasattr(feed.feed, 'title') else urlparse(feed_url).netloc,
                        published_date=published_date,
                        author=entry.author if hasattr(entry, 'author') else None,
                        summary=content[:500] + "..." if len(content) > 500 else content
                    )
                    
                    articles.append(article)
                    
                except Exception as e:
                    logger.warning(f"Failed to parse RSS entry: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to parse RSS feed {feed_url}: {str(e)}")
            
        return articles

    def _clean_html(self, html_content: str) -> str:
        """Clean HTML content to plain text"""
        if not html_content:
            return ""
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean whitespace
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            logger.warning(f"Failed to clean HTML: {str(e)}")
            return html_content

    def calculate_relevance_score(self, article: NewsArticle, search_terms: List[str]) -> float:
        """Calculate relevance score for an article based on search terms"""
        score = 0.0
        text = (article.title + " " + article.content).lower()
        
        for term in search_terms:
            term_lower = term.lower()
            # Title mentions are worth more
            title_mentions = article.title.lower().count(term_lower)
            content_mentions = article.content.lower().count(term_lower)
            
            score += (title_mentions * 2.0) + (content_mentions * 1.0)
        
        # Normalize by content length
        if len(text) > 0:
            score = score / (len(text) / 1000.0)  # Per 1000 characters
            
        return min(score, 10.0)  # Cap at 10

    def search_microsoft_news(self, max_articles_per_source: int = 10) -> List[NewsArticle]:
        """Search for Microsoft-related news across all sources"""
        all_articles = []
        
        for source_key, source_config in self.news_sources.items():
            logger.info(f"Fetching articles from {source_config['name']}")
            
            for feed_url in source_config.get('rss_feeds', []):
                articles = self.get_rss_articles(feed_url, max_articles_per_source)
                
                # Filter for Microsoft relevance
                for article in articles:
                    relevance = self.calculate_relevance_score(article, self.microsoft_keywords)
                    if relevance > 0.5:  # Only include articles with decent relevance
                        article.relevance_score = relevance
                        all_articles.append(article)
        
        # Sort by relevance and date
        all_articles.sort(key=lambda x: (x.relevance_score, x.published_date or datetime.min), reverse=True)
        
        logger.info(f"Found {len(all_articles)} Microsoft-related articles")
        return all_articles

    def search_competitor_news(self, competitor: str = None, max_articles_per_source: int = 10) -> Dict[str, List[NewsArticle]]:
        """Search for competitor news"""
        competitor_articles = {}
        
        # If specific competitor is requested
        if competitor and competitor.lower() in self.competitor_keywords:
            competitors_to_search = {competitor.lower(): self.competitor_keywords[competitor.lower()]}
        else:
            # Search all competitors
            competitors_to_search = self.competitor_keywords
        
        for comp_name, keywords in competitors_to_search.items():
            competitor_articles[comp_name] = []
            
            for source_key, source_config in self.news_sources.items():
                logger.info(f"Fetching {comp_name} articles from {source_config['name']}")
                
                for feed_url in source_config.get('rss_feeds', []):
                    articles = self.get_rss_articles(feed_url, max_articles_per_source)
                    
                    # Filter for competitor relevance
                    for article in articles:
                        relevance = self.calculate_relevance_score(article, keywords)
                        if relevance > 0.5:
                            article.relevance_score = relevance
                            competitor_articles[comp_name].append(article)
            
            # Sort competitor articles
            competitor_articles[comp_name].sort(
                key=lambda x: (x.relevance_score, x.published_date or datetime.min), 
                reverse=True
            )
            
            logger.info(f"Found {len(competitor_articles[comp_name])} {comp_name} articles")
        
        return competitor_articles

    def search_market_trends(self, industry_keywords: List[str], max_articles_per_source: int = 15) -> List[NewsArticle]:
        """Search for market trends and industry analysis"""
        all_articles = []
        
        # Default industry keywords if none provided
        if not industry_keywords:
            industry_keywords = [
                'cloud computing', 'artificial intelligence', 'machine learning',
                'digital transformation', 'cybersecurity', 'data analytics',
                'remote work', 'collaboration software', 'enterprise software'
            ]
        
        for source_key, source_config in self.news_sources.items():
            logger.info(f"Fetching market trends from {source_config['name']}")
            
            for feed_url in source_config.get('rss_feeds', []):
                articles = self.get_rss_articles(feed_url, max_articles_per_source)
                
                # Filter for market trend relevance
                for article in articles:
                    relevance = self.calculate_relevance_score(article, industry_keywords)
                    if relevance > 0.3:  # Lower threshold for market trends
                        article.relevance_score = relevance
                        all_articles.append(article)
        
        # Sort by relevance and date
        all_articles.sort(key=lambda x: (x.relevance_score, x.published_date or datetime.min), reverse=True)
        
        logger.info(f"Found {len(all_articles)} market trend articles")
        return all_articles

    def get_comprehensive_market_intelligence(self, 
                                            include_microsoft: bool = True,
                                            include_competitors: bool = True,
                                            include_market_trends: bool = True,
                                            max_articles_per_category: int = 15) -> Dict[str, any]:
        """Get comprehensive market intelligence including Microsoft, competitors, and market trends"""
        
        intelligence_data = {
            'microsoft_news': [],
            'competitor_news': {},
            'market_trends': [],
            'summary': {},
            'last_updated': datetime.now().isoformat()
        }
        
        logger.info("Starting comprehensive market intelligence gathering")
        
        try:
            # Get Microsoft news
            if include_microsoft:
                logger.info("Gathering Microsoft news...")
                microsoft_articles = self.search_microsoft_news(max_articles_per_category)
                intelligence_data['microsoft_news'] = [
                    {
                        'title': article.title,
                        'url': article.url,
                        'content': article.content[:1000],  # Truncate for summary
                        'source': article.source,
                        'published_date': article.published_date.isoformat() if article.published_date else None,
                        'relevance_score': article.relevance_score,
                        'summary': article.summary
                    }
                    for article in microsoft_articles[:max_articles_per_category]
                ]
            
            # Get competitor news
            if include_competitors:
                logger.info("Gathering competitor news...")
                competitor_articles = self.search_competitor_news(max_articles_per_source=max_articles_per_category)
                for comp_name, articles in competitor_articles.items():
                    intelligence_data['competitor_news'][comp_name] = [
                        {
                            'title': article.title,
                            'url': article.url,
                            'content': article.content[:1000],
                            'source': article.source,
                            'published_date': article.published_date.isoformat() if article.published_date else None,
                            'relevance_score': article.relevance_score,
                            'summary': article.summary
                        }
                        for article in articles[:max_articles_per_category]
                    ]
            
            # Get market trends
            if include_market_trends:
                logger.info("Gathering market trends...")
                trend_articles = self.search_market_trends([], max_articles_per_category)
                intelligence_data['market_trends'] = [
                    {
                        'title': article.title,
                        'url': article.url,
                        'content': article.content[:1000],
                        'source': article.source,
                        'published_date': article.published_date.isoformat() if article.published_date else None,
                        'relevance_score': article.relevance_score,
                        'summary': article.summary
                    }
                    for article in trend_articles[:max_articles_per_category]
                ]
            
            # Generate summary statistics
            intelligence_data['summary'] = {
                'total_microsoft_articles': len(intelligence_data['microsoft_news']),
                'total_competitor_articles': sum(len(articles) for articles in intelligence_data['competitor_news'].values()),
                'total_market_trend_articles': len(intelligence_data['market_trends']),
                'competitors_covered': list(intelligence_data['competitor_news'].keys()),
                'data_freshness': 'Real-time from RSS feeds',
                'sources_covered': list(set([source['name'] for source in self.news_sources.values()]))
            }
            
            logger.info(f"Market intelligence gathering completed. Summary: {intelligence_data['summary']}")
            
        except Exception as e:
            logger.error(f"Error in comprehensive market intelligence gathering: {str(e)}")
            intelligence_data['error'] = str(e)
        
        return intelligence_data

    def format_articles_for_analysis(self, articles: List[NewsArticle], max_length: int = 2000) -> str:
        """Format articles for AI analysis"""
        formatted_content = ""
        
        for i, article in enumerate(articles[:10], 1):  # Limit to top 10 articles
            article_text = f"""
ARTICLE {i}:
Title: {article.title}
Source: {article.source}
Date: {article.published_date.strftime('%Y-%m-%d') if article.published_date else 'Unknown'}
Content: {article.content[:max_length]}
URL: {article.url}
Relevance Score: {article.relevance_score:.2f}

---
"""
            formatted_content += article_text
        
        return formatted_content

# Convenience functions for backward compatibility
def get_microsoft_market_intelligence() -> Dict[str, any]:
    """Get Microsoft-focused market intelligence"""
    service = WebScrapingService()
    return service.get_comprehensive_market_intelligence(
        include_microsoft=True,
        include_competitors=True,
        include_market_trends=True
    )

def get_competitor_analysis(competitor: str = None) -> Dict[str, List[NewsArticle]]:
    """Get competitor analysis"""
    service = WebScrapingService()
    return service.search_competitor_news(competitor)

def get_latest_market_trends(industry_keywords: List[str] = None) -> List[NewsArticle]:
    """Get latest market trends"""
    service = WebScrapingService()
    return service.search_market_trends(industry_keywords or [])
