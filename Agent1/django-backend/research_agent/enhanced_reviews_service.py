"""
Enhanced Customer Reviews Service with Anti-Bot Protection
Uses sophisticated techniques to gather real customer feedback daily
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
import logging
from bs4 import BeautifulSoup
import random
from pathlib import Path
import feedparser
from urllib.parse import quote_plus
import hashlib

class EnhancedReviewsService:
    """Enhanced service for gathering real customer reviews with daily updates"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache_dir = Path('cache/reviews')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Rotating user agents and headers
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36'
        ]
        
        # Alternative sources that are more accessible
        self.sources = {
            'reddit_feeds': {
                'cybersecurity': 'https://www.reddit.com/r/cybersecurity.rss',
                'sysadmin': 'https://www.reddit.com/r/sysadmin.rss',
                'security': 'https://www.reddit.com/r/security.rss',
                'ITManagers': 'https://www.reddit.com/r/ITManagers.rss'
            },
            'tech_forums': {
                'spiceworks': 'https://community.spiceworks.com/rss/discussions',
                'serverfault': 'https://serverfault.com/feeds',
                'stackoverflow': 'https://stackoverflow.com/feeds/tag/cybersecurity'
            },
            'github_discussions': {
                'security_tools': 'https://api.github.com/search/issues?q=microsoft+defender+office+365+type:issue',
                'crowdstrike': 'https://api.github.com/search/issues?q=crowdstrike+falcon+type:issue',
                'proofpoint': 'https://api.github.com/search/issues?q=proofpoint+email+security+type:issue'
            }
        }
    
    def fetch_daily_reviews(self, product_name: str, max_reviews: int = 30) -> List[Dict]:
        """Fetch reviews from multiple accessible sources daily"""
        
        # Check cache first
        cached_reviews = self.get_cached_reviews(product_name)
        if cached_reviews and self.is_cache_fresh(product_name, max_age_hours=12):
            self.logger.info(f"📊 Using fresh cached reviews for {product_name}: {len(cached_reviews)} reviews")
            return cached_reviews[:max_reviews]
        
        self.logger.info(f"🔄 Fetching fresh reviews for {product_name}...")
        all_reviews = []
        
        try:
            # Method 1: RSS Feeds from forums and Reddit
            rss_reviews = self.fetch_rss_reviews(product_name, max_reviews=15)
            all_reviews.extend(rss_reviews)
            
            time.sleep(1)
            
            # Method 2: GitHub Issues and Discussions
            github_reviews = self.fetch_github_discussions(product_name, max_reviews=10)
            all_reviews.extend(github_reviews)
            
            time.sleep(1)
            
            # Method 3: Alternative Review Sites
            alt_reviews = self.fetch_alternative_reviews(product_name, max_reviews=10)
            all_reviews.extend(alt_reviews)
            
            # Method 4: Product Documentation and Changelogs (user feedback)
            doc_reviews = self.fetch_documentation_feedback(product_name, max_reviews=5)
            all_reviews.extend(doc_reviews)
            
            # Remove duplicates and sort
            unique_reviews = self.deduplicate_reviews(all_reviews)
            unique_reviews.sort(key=lambda x: (x.get('date_scraped', ''), x.get('rating', 0)), reverse=True)
            
            if unique_reviews:
                self.cache_reviews(product_name, unique_reviews)
                self.logger.info(f"✅ Fetched and cached {len(unique_reviews)} fresh reviews for {product_name}")
            
            return unique_reviews[:max_reviews]
            
        except Exception as e:
            self.logger.error(f"Error fetching reviews for {product_name}: {e}")
            return cached_reviews[:max_reviews] if cached_reviews else []
    
    def fetch_rss_reviews(self, product_name: str, max_reviews: int = 15) -> List[Dict]:
        """Fetch reviews from RSS feeds (Reddit, forums)"""
        reviews = []
        keywords = self.get_product_keywords(product_name)
        
        try:
            for source_name, rss_url in self.sources['reddit_feeds'].items():
                try:
                    self.logger.info(f"🔍 Fetching RSS from {source_name}: {rss_url}")
                    feed = feedparser.parse(rss_url)
                    
                    for entry in feed.entries[:20]:  # Check recent 20 posts
                        title = entry.get('title', '').lower()
                        summary = entry.get('summary', '').lower()
                        content = title + ' ' + summary
                        
                        # Check if post mentions our product
                        if any(keyword.lower() in content for keyword in keywords):
                            # Analyze sentiment
                            sentiment_score = self.analyze_content_sentiment(content)
                            rating = self.sentiment_to_rating(sentiment_score)
                            
                            review = {
                                'platform': f'Reddit r/{source_name}',
                                'product': product_name,
                                'rating': rating,
                                'review_text': f"{entry.get('title', '')}\n\n{entry.get('summary', '')[:300]}",
                                'reviewer': f"Reddit User",
                                'source_url': entry.get('link', ''),
                                'date_scraped': datetime.now().isoformat(),
                                'content_type': 'reddit_rss_feed',
                                'verified': True,
                                'scraping_source': 'rss_feed'
                            }
                            reviews.append(review)
                            
                            if len(reviews) >= max_reviews:
                                break
                    
                    time.sleep(0.5)  # Be respectful
                    
                except Exception as e:
                    self.logger.warning(f"Error fetching RSS from {source_name}: {e}")
                    continue
            
            self.logger.info(f"✅ Fetched {len(reviews)} reviews from RSS feeds for {product_name}")
            
        except Exception as e:
            self.logger.error(f"Error fetching RSS reviews: {e}")
        
        return reviews
    
    def fetch_github_discussions(self, product_name: str, max_reviews: int = 10) -> List[Dict]:
        """Fetch discussions from GitHub issues and repositories"""
        reviews = []
        keywords = self.get_product_keywords(product_name)
        
        try:
            # Search GitHub for issues mentioning the product
            query = ' OR '.join(keywords[:3])  # Use top 3 keywords
            search_url = f"https://api.github.com/search/issues?q={quote_plus(query)}&sort=updated&per_page=20"
            
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': random.choice(self.user_agents)
            }
            
            response = requests.get(search_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('items', [])
                
                for issue in issues[:max_reviews]:
                    try:
                        title = issue.get('title', '')
                        body = issue.get('body', '') or ''
                        content = f"{title} {body}"
                        
                        # Filter for relevant discussions
                        if any(keyword.lower() in content.lower() for keyword in keywords):
                            sentiment_score = self.analyze_content_sentiment(content)
                            rating = self.sentiment_to_rating(sentiment_score)
                            
                            review = {
                                'platform': 'GitHub Issues',
                                'product': product_name,
                                'rating': rating,
                                'review_text': f"{title}\n\n{body[:400]}",
                                'reviewer': issue.get('user', {}).get('login', 'GitHub User'),
                                'source_url': issue.get('html_url', ''),
                                'date_scraped': datetime.now().isoformat(),
                                'content_type': 'github_discussion',
                                'verified': True,
                                'scraping_source': 'github_api'
                            }
                            reviews.append(review)
                    
                    except Exception as e:
                        self.logger.warning(f"Error processing GitHub issue: {e}")
                        continue
            
            self.logger.info(f"✅ Fetched {len(reviews)} reviews from GitHub for {product_name}")
            
        except Exception as e:
            self.logger.error(f"Error fetching GitHub discussions: {e}")
        
        return reviews
    
    def fetch_alternative_reviews(self, product_name: str, max_reviews: int = 10) -> List[Dict]:
        """Fetch from alternative accessible sources"""
        reviews = []
        
        try:
            # Method: Search for blog posts and articles mentioning the product
            keywords = self.get_product_keywords(product_name)
            
            # Use alternative search approaches
            search_sources = [
                f"https://hn.algolia.com/api/v1/search?query={quote_plus(keywords[0])}&tags=story",  # Hacker News
                f"https://www.reddit.com/search.json?q={quote_plus(keywords[0])}&sort=new&limit=10"  # Reddit API
            ]
            
            for source_url in search_sources:
                try:
                    headers = {'User-Agent': random.choice(self.user_agents)}
                    response = requests.get(source_url, headers=headers, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if 'hits' in data:  # Hacker News format
                            items = data['hits']
                        elif 'data' in data:  # Reddit format
                            items = data['data'].get('children', [])
                        else:
                            continue
                        
                        for item in items[:5]:
                            try:
                                if 'hits' in data:  # Hacker News
                                    title = item.get('title', '')
                                    text = item.get('story_text', '') or ''
                                    url = item.get('url', '')
                                    author = item.get('author', 'HN User')
                                else:  # Reddit
                                    item_data = item.get('data', {})
                                    title = item_data.get('title', '')
                                    text = item_data.get('selftext', '') or ''
                                    url = f"https://reddit.com{item_data.get('permalink', '')}"
                                    author = item_data.get('author', 'Reddit User')
                                
                                content = f"{title} {text}"
                                if any(keyword.lower() in content.lower() for keyword in keywords):
                                    sentiment_score = self.analyze_content_sentiment(content)
                                    rating = self.sentiment_to_rating(sentiment_score)
                                    
                                    review = {
                                        'platform': 'Tech Community',
                                        'product': product_name,
                                        'rating': rating,
                                        'review_text': f"{title}\n\n{text[:300]}",
                                        'reviewer': author,
                                        'source_url': url,
                                        'date_scraped': datetime.now().isoformat(),
                                        'content_type': 'community_discussion',
                                        'verified': True,
                                        'scraping_source': 'alternative_api'
                                    }
                                    reviews.append(review)
                            
                            except Exception as e:
                                self.logger.warning(f"Error processing alternative source item: {e}")
                                continue
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    self.logger.warning(f"Error fetching from alternative source {source_url}: {e}")
                    continue
            
            self.logger.info(f"✅ Fetched {len(reviews)} reviews from alternative sources for {product_name}")
            
        except Exception as e:
            self.logger.error(f"Error fetching alternative reviews: {e}")
        
        return reviews
    
    def fetch_documentation_feedback(self, product_name: str, max_reviews: int = 5) -> List[Dict]:
        """Fetch user feedback from documentation and change logs"""
        reviews = []
        
        try:
            # Microsoft documentation often has user comments
            if 'microsoft' in product_name.lower():
                # Search for Microsoft Docs pages
                docs_urls = [
                    "https://docs.microsoft.com/en-us/microsoft-365/security/office-365-security/",
                    "https://techcommunity.microsoft.com/",
                ]
                
                for url in docs_urls:
                    try:
                        headers = {'User-Agent': random.choice(self.user_agents)}
                        response = requests.get(url, headers=headers, timeout=30)
                        
                        if response.status_code == 200:
                            # Look for user feedback or comments in the page
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            # Find comment-like elements
                            comment_elements = soup.find_all(['div', 'section'], 
                                                           class_=re.compile(r'comment|feedback|review', re.I))
                            
                            for element in comment_elements[:max_reviews]:
                                text = element.get_text(strip=True)
                                if len(text) > 50 and any(keyword.lower() in text.lower() 
                                                        for keyword in self.get_product_keywords(product_name)):
                                    sentiment_score = self.analyze_content_sentiment(text)
                                    rating = self.sentiment_to_rating(sentiment_score)
                                    
                                    review = {
                                        'platform': 'Microsoft Documentation',
                                        'product': product_name,
                                        'rating': rating,
                                        'review_text': text[:400],
                                        'reviewer': 'Microsoft Community User',
                                        'source_url': url,
                                        'date_scraped': datetime.now().isoformat(),
                                        'content_type': 'documentation_feedback',
                                        'verified': True,
                                        'scraping_source': 'documentation'
                                    }
                                    reviews.append(review)
                    
                    except Exception as e:
                        self.logger.warning(f"Error fetching documentation feedback from {url}: {e}")
                        continue
            
        except Exception as e:
            self.logger.error(f"Error fetching documentation feedback: {e}")
        
        return reviews
    
    def get_product_keywords(self, product_name: str) -> List[str]:
        """Get relevant keywords for searching"""
        keyword_map = {
            'Microsoft Defender for Office 365': [
                'Microsoft Defender Office 365', 'MDO', 'Defender ATP', 
                'Office 365 security', 'Microsoft 365 Defender', 'ATP Office 365'
            ],
            'Proofpoint': [
                'Proofpoint', 'Proofpoint email security', 'Proofpoint protection',
                'Proofpoint TAP', 'Proofpoint Email Protection'
            ],
            'Mimecast': [
                'Mimecast', 'Mimecast email security', 'Mimecast protection',
                'Mimecast gateway'
            ],
            'CrowdStrike': [
                'CrowdStrike', 'CrowdStrike Falcon', 'Falcon endpoint',
                'CrowdStrike EDR', 'Falcon platform'
            ],
            'SentinelOne': [
                'SentinelOne', 'Sentinel One', 'SentinelOne endpoint',
                'S1 endpoint', 'SentinelOne Singularity'
            ]
        }
        
        return keyword_map.get(product_name, [product_name])
    
    def analyze_content_sentiment(self, text: str) -> float:
        """Simple sentiment analysis without external dependencies"""
        positive_words = [
            'excellent', 'great', 'good', 'love', 'amazing', 'fantastic',
            'wonderful', 'perfect', 'outstanding', 'impressive', 'reliable',
            'effective', 'efficient', 'useful', 'helpful', 'solid', 'strong'
        ]
        
        negative_words = [
            'terrible', 'awful', 'bad', 'hate', 'horrible', 'disappointing',
            'poor', 'worst', 'useless', 'broken', 'slow', 'unreliable',
            'ineffective', 'problematic', 'issues', 'bugs', 'crashes'
        ]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / max(1, total_words / 100)
        return max(-1.0, min(1.0, sentiment))  # Clamp to [-1, 1]
    
    def sentiment_to_rating(self, sentiment: float) -> int:
        """Convert sentiment to 1-5 rating"""
        if sentiment >= 0.3:
            return 5
        elif sentiment >= 0.1:
            return 4
        elif sentiment >= -0.1:
            return 3
        elif sentiment >= -0.3:
            return 2
        else:
            return 1
    
    def deduplicate_reviews(self, reviews: List[Dict]) -> List[Dict]:
        """Remove duplicate reviews based on content similarity"""
        unique_reviews = []
        seen_hashes = set()
        
        for review in reviews:
            # Create a hash of the review content
            content = f"{review.get('platform', '')}{review.get('review_text', '')}"
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            if content_hash not in seen_hashes:
                unique_reviews.append(review)
                seen_hashes.add(content_hash)
        
        return unique_reviews
    
    def cache_reviews(self, product_name: str, reviews: List[Dict]):
        """Cache reviews with metadata"""
        cache_file = self.cache_dir / f"{self._sanitize_filename(product_name)}_reviews.json"
        
        cache_data = {
            'product': product_name,
            'last_updated': datetime.now().isoformat(),
            'total_reviews': len(reviews),
            'reviews': reviews,
            'source_platforms': list(set(r.get('platform', 'Unknown') for r in reviews)),
            'cache_version': '3.0',
            'scraping_methods': list(set(r.get('scraping_source', 'unknown') for r in reviews))
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error caching reviews for {product_name}: {e}")
    
    def get_cached_reviews(self, product_name: str) -> List[Dict]:
        """Get cached reviews"""
        cache_file = self.cache_dir / f"{self._sanitize_filename(product_name)}_reviews.json"
        
        try:
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('reviews', [])
        except Exception as e:
            self.logger.warning(f"Error loading cached reviews for {product_name}: {e}")
        
        return []
    
    def is_cache_fresh(self, product_name: str, max_age_hours: int = 12) -> bool:
        """Check if cache is fresh"""
        cache_file = self.cache_dir / f"{self._sanitize_filename(product_name)}_reviews.json"
        
        try:
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    last_updated = datetime.fromisoformat(data.get('last_updated', ''))
                    age_hours = (datetime.now() - last_updated).total_seconds() / 3600
                    return age_hours < max_age_hours
        except Exception as e:
            self.logger.warning(f"Error checking cache freshness for {product_name}: {e}")
        
        return False
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename"""
        return re.sub(r'[^\w\-_.]', '_', filename).lower()
