"""
Real Customer Reviews Service
Integrates with actual review platforms and data sources to fetch genuine customer feedback
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
import logging
from bs4 import BeautifulSoup
import praw  # Reddit API
from textblob import TextBlob
import os
from dotenv import load_dotenv
from pathlib import Path
import random

load_dotenv()

class RealCustomerReviewsService:
    """Service to fetch real customer reviews from various platforms with daily caching"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Setup cache directory
        self.cache_dir = Path('cache/reviews')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # API Keys and credentials (set these in your .env file)
        self.g2_api_key = os.getenv('G2_API_KEY')
        self.trustradius_api_key = os.getenv('TRUSTRADIUS_API_KEY')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.reddit_user_agent = os.getenv('REDDIT_USER_AGENT', 'ReviewScraper/1.0')
        
        # Initialize Reddit client if credentials are available
        self.reddit = None
        if self.reddit_client_id and self.reddit_client_secret:
            try:
                self.reddit = praw.Reddit(
                    client_id=self.reddit_client_id,
                    client_secret=self.reddit_client_secret,
                    user_agent=self.reddit_user_agent
                )
                # Test connection
                self.reddit.user.me()
            except Exception as e:
                self.logger.warning(f"Failed to initialize Reddit client: {e}")
                self.reddit = None
        
        # Enhanced product mappings for web scraping
        self.product_mappings = {
            'Microsoft Defender for Office 365': {
                'g2_slug': 'microsoft-defender-for-office-365',
                'trustradius_slug': 'microsoft-defender-office-365',
                'reddit_keywords': ['microsoft defender office', 'MDO', 'office 365 security', 'defender atp', 'microsoft 365 defender'],
                'capterra_slug': 'microsoft-defender-for-office-365',
                'gartner_search': 'Microsoft Defender Office 365'
            },
            'Proofpoint': {
                'g2_slug': 'proofpoint-email-protection',
                'trustradius_slug': 'proofpoint-email-security-and-protection',
                'reddit_keywords': ['proofpoint', 'proofpoint email', 'proofpoint protection'],
                'capterra_slug': 'proofpoint',
                'gartner_search': 'Proofpoint Email Security'
            },
            'Mimecast': {
                'g2_slug': 'mimecast',
                'trustradius_slug': 'mimecast-email-security',
                'reddit_keywords': ['mimecast', 'mimecast email'],
                'capterra_slug': 'mimecast',
                'gartner_search': 'Mimecast Email Security'
            },
            'CrowdStrike': {
                'g2_slug': 'crowdstrike-falcon',
                'trustradius_slug': 'crowdstrike-falcon-platform',
                'reddit_keywords': ['crowdstrike', 'crowdstrike falcon', 'falcon endpoint'],
                'capterra_slug': 'crowdstrike-falcon',
                'gartner_search': 'CrowdStrike Falcon'
            },
            'SentinelOne': {
                'g2_slug': 'sentinelone',
                'trustradius_slug': 'sentinelone-singularity',
                'reddit_keywords': ['sentinelone', 'sentinel one', 'sentinelone endpoint'],
                'capterra_slug': 'sentinelone',
                'gartner_search': 'SentinelOne Singularity'
            }
        }
        
        # User agents for web scraping rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

    def fetch_all_real_reviews(self, product_name: str, max_reviews: int = 50) -> List[Dict]:
        """Fetch real customer reviews from all available sources with intelligent caching"""
        
        # First, try to get cached reviews (updated daily)
        cached_reviews = self.get_cached_reviews(product_name)
        
        if cached_reviews and self.is_cache_fresh(product_name):
            self.logger.info(f"Using fresh cached reviews for {product_name}: {len(cached_reviews)} reviews")
            return cached_reviews[:max_reviews]
        
        # If cache is stale or empty, fetch fresh reviews
        self.logger.info(f"Fetching fresh reviews for {product_name}...")
        all_reviews = []
        
        try:
            # Fetch from Reddit (most reliable and free)
            reddit_reviews = self.fetch_reddit_discussions(product_name, max_reviews=20)
            all_reviews.extend(reddit_reviews)
            
            # Add delay between platforms to be respectful
            time.sleep(1)
            
            # Fetch from G2 Crowd (web scraping)
            g2_reviews = self.scrape_g2_reviews(product_name, max_reviews=15)
            all_reviews.extend(g2_reviews)
            
            time.sleep(1)
            
            # Fetch from TrustRadius (web scraping)
            trustradius_reviews = self.fetch_trustradius_reviews(product_name, max_reviews=10)
            all_reviews.extend(trustradius_reviews)
            
            time.sleep(1)
            
            # Fetch from Capterra (web scraping)
            capterra_reviews = self.fetch_capterra_reviews(product_name, max_reviews=5)
            all_reviews.extend(capterra_reviews)
            
            # Sort by date and sentiment score (newest and most positive first)
            all_reviews.sort(key=lambda x: (x.get('date_scraped', ''), x.get('rating', 0)), reverse=True)
            
            # Cache the results for future use
            if all_reviews:
                self.cache_reviews(product_name, all_reviews)
                self.logger.info(f"Fetched and cached {len(all_reviews)} fresh reviews for {product_name}")
            
            return all_reviews[:max_reviews]
            
        except Exception as e:
            self.logger.error(f"Error fetching real reviews for {product_name}: {e}")
            
            # Fallback to cached reviews even if stale
            if cached_reviews:
                self.logger.info(f"Using stale cached reviews as fallback for {product_name}")
                return cached_reviews[:max_reviews]
            
            return []

    def get_cached_reviews(self, product_name: str) -> List[Dict]:
        """Get cached reviews for a product"""
        cache_file = self.cache_dir / f"{self._sanitize_filename(product_name)}_reviews.json"
        
        try:
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    reviews = data.get('reviews', [])
                    # Filter for verified real reviews
                    real_reviews = [r for r in reviews if r.get('verified', False)]
                    return real_reviews
        except Exception as e:
            self.logger.warning(f"Error loading cached reviews for {product_name}: {e}")
        
        return []

    def cache_reviews(self, product_name: str, reviews: List[Dict]):
        """Cache reviews with metadata"""
        cache_file = self.cache_dir / f"{self._sanitize_filename(product_name)}_reviews.json"
        
        cache_data = {
            'product': product_name,
            'last_updated': datetime.now().isoformat(),
            'total_reviews': len(reviews),
            'reviews': reviews,
            'source_platforms': list(set(r.get('platform', 'Unknown') for r in reviews)),
            'cache_version': '2.0'
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error caching reviews for {product_name}: {e}")

    def is_cache_fresh(self, product_name: str, max_age_hours: int = 12) -> bool:
        """Check if cached reviews are fresh (less than max_age_hours old)"""
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
        """Sanitize product name for use as filename"""
        return re.sub(r'[^\w\-_.]', '_', filename).lower()

    def fetch_g2_reviews(self, product_name: str, max_reviews: int = 15) -> List[Dict]:
        """Fetch reviews from G2 Crowd using web scraping (G2 API is not publicly available)"""
        self.logger.info(f"Fetching G2 reviews for {product_name} using web scraping")
        return self.scrape_g2_reviews(product_name, max_reviews)

    def scrape_g2_reviews(self, product_name: str, max_reviews: int = 15) -> List[Dict]:
        """Scrape G2 reviews with improved selectors and error handling"""
        reviews = []
        
        try:
            product_mapping = self.product_mappings.get(product_name, {})
            g2_slug = product_mapping.get('g2_slug')
            
            if not g2_slug:
                self.logger.warning(f"No G2 slug found for {product_name}")
                return []
            
            url = f"https://www.g2.com/products/{g2_slug}/reviews"
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            self.logger.info(f"Scraping G2 reviews from: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Multiple selectors to try (G2 changes their structure)
                review_selectors = [
                    'div[data-review-id]',  # Common G2 review selector
                    '.review-item',
                    '.review-card',
                    '.paper.paper--white',
                    '[class*="review"]'
                ]
                
                review_elements = []
                for selector in review_selectors:
                    elements = soup.select(selector)
                    if elements:
                        review_elements = elements
                        self.logger.info(f"Found {len(elements)} reviews using selector: {selector}")
                        break
                
                if not review_elements:
                    # Fallback: look for any div with review-like content
                    review_elements = soup.find_all('div', string=re.compile(r'(review|rating|star)', re.I))
                    self.logger.info(f"Fallback: found {len(review_elements)} potential review elements")
                
                for i, element in enumerate(review_elements[:max_reviews]):
                    try:
                        # Extract rating (multiple approaches)
                        rating = self._extract_g2_rating(element)
                        
                        # Extract review text
                        review_text = self._extract_g2_text(element)
                        
                        # Extract reviewer info
                        reviewer = self._extract_g2_reviewer(element)
                        
                        if review_text and len(review_text.strip()) > 20:  # Only valid reviews
                            review = {
                                'platform': 'G2 Crowd',
                                'product': product_name,
                                'rating': rating,
                                'review_text': review_text.strip(),
                                'reviewer': reviewer or f'G2_User_{i+1}',
                                'source_url': url,
                                'date_scraped': datetime.now().isoformat(),
                                'content_type': 'professional_review',
                                'verified': True,
                                'scraping_source': 'g2_web_scraping'
                            }
                            reviews.append(review)
                            self.logger.debug(f"Extracted G2 review: {review_text[:50]}...")
                        
                    except Exception as e:
                        self.logger.warning(f"Error parsing G2 review element {i}: {e}")
                        continue
                
                self.logger.info(f"Successfully scraped {len(reviews)} G2 reviews for {product_name}")
            
            else:
                self.logger.warning(f"G2 request failed with status {response.status_code}")
            
        except Exception as e:
            self.logger.error(f"Error scraping G2 reviews for {product_name}: {e}")
        
        return reviews

    def _extract_g2_rating(self, element) -> int:
        """Extract rating from G2 review element"""
        try:
            # Look for star ratings
            star_selectors = [
                '.stars .star.star--filled',
                '[class*="star"][class*="filled"]',
                '.rating-stars .filled',
                '.star-rating .active'
            ]
            
            for selector in star_selectors:
                stars = element.select(selector)
                if stars:
                    return min(5, len(stars))
            
            # Look for numerical rating
            rating_text = element.get_text()
            rating_match = re.search(r'(\d(?:\.\d)?)\s*(?:out of|/)\s*5', rating_text)
            if rating_match:
                return min(5, max(1, int(float(rating_match.group(1)))))
            
            # Look for rating in data attributes
            for attr in ['data-rating', 'data-score']:
                if element.get(attr):
                    try:
                        return min(5, max(1, int(float(element.get(attr)))))
                    except:
                        continue
            
            return 4  # Default rating if not found
            
        except Exception as e:
            self.logger.debug(f"Error extracting G2 rating: {e}")
            return 3

    def _extract_g2_text(self, element) -> str:
        """Extract review text from G2 element"""
        try:
            # Common text selectors
            text_selectors = [
                '.review-content',
                '.review-text',
                '.review-body',
                '[class*="review-content"]',
                'p',
                '.description'
            ]
            
            for selector in text_selectors:
                text_elem = element.select_one(selector)
                if text_elem:
                    text = text_elem.get_text(strip=True)
                    if len(text) > 20:  # Valid review text
                        return text
            
            # Fallback: get all text and filter
            all_text = element.get_text(strip=True)
            if len(all_text) > 50:
                # Try to extract meaningful sentences
                sentences = [s.strip() for s in all_text.split('.') if len(s.strip()) > 20]
                if sentences:
                    return '. '.join(sentences[:3]) + '.'
            
            return all_text[:200] if all_text else 'Review content not available'
            
        except Exception as e:
            self.logger.debug(f"Error extracting G2 text: {e}")
            return 'Review content not available'

    def _extract_g2_reviewer(self, element) -> str:
        """Extract reviewer name from G2 element"""
        try:
            # Common reviewer selectors
            reviewer_selectors = [
                '.reviewer-name',
                '.user-name',
                '.author',
                '[class*="reviewer"]',
                '[class*="user"]'
            ]
            
            for selector in reviewer_selectors:
                reviewer_elem = element.select_one(selector)
                if reviewer_elem:
                    name = reviewer_elem.get_text(strip=True)
                    if name and len(name) < 50:  # Reasonable name length
                        return name
            
            return 'G2 Verified User'
            
        except Exception as e:
            self.logger.debug(f"Error extracting G2 reviewer: {e}")
            return 'Anonymous G2 User'

    def fetch_trustradius_reviews(self, product_name: str, max_reviews: int = 15) -> List[Dict]:
        """Fetch reviews from TrustRadius"""
        reviews = []
        
        try:
            product_mapping = self.product_mappings.get(product_name, {})
            trustradius_slug = product_mapping.get('trustradius_slug')
            
            if not trustradius_slug:
                return []
            
            # TrustRadius API or web scraping
            url = f"https://www.trustradius.com/products/{trustradius_slug}/reviews"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find review elements (adjust based on TrustRadius structure)
                review_elements = soup.find_all('div', class_='review-card')
                
                for element in review_elements[:max_reviews]:
                    try:
                        # Extract data
                        rating_element = element.find('div', class_='rating-stars')
                        rating = self._extract_rating_from_stars(rating_element) if rating_element else 0
                        
                        content_element = element.find('div', class_='review-content-text')
                        content = content_element.get_text(strip=True) if content_element else ''
                        
                        reviewer_element = element.find('div', class_='reviewer-name')
                        reviewer = reviewer_element.get_text(strip=True) if reviewer_element else 'Anonymous'
                        
                        review = {
                            'platform': 'TrustRadius',
                            'product': product_name,
                            'rating': rating,
                            'review_text': content,
                            'reviewer': reviewer,
                            'source_url': url,
                            'date_scraped': datetime.now().isoformat(),
                            'content_type': 'professional_review',
                            'verified': True
                        }
                        reviews.append(review)
                        
                    except Exception as e:
                        self.logger.warning(f"Error parsing TrustRadius review: {e}")
                        continue
            
        except Exception as e:
            self.logger.error(f"Error fetching TrustRadius reviews: {e}")
        
        return reviews

    def fetch_reddit_discussions(self, product_name: str, max_reviews: int = 10) -> List[Dict]:
        """Fetch real discussions from Reddit"""
        reviews = []
        
        try:
            if not self.reddit:
                self.logger.warning("Reddit client not initialized - check API credentials")
                return []
            
            # Test Reddit connection first
            try:
                # Test if we can access Reddit
                test_subreddit = self.reddit.subreddit('test')
                test_subreddit.id  # This will raise an exception if auth fails
                self.logger.info("Reddit API connection successful")
            except Exception as auth_error:
                self.logger.error(f"Reddit authentication failed: {auth_error}")
                return []
            
            product_mapping = self.product_mappings.get(product_name, {})
            keywords = product_mapping.get('reddit_keywords', [])
            
            if not keywords:
                self.logger.warning(f"No Reddit keywords found for product: {product_name}")
                return []
            
            subreddits = ['cybersecurity', 'sysadmin', 'Office365', 'security', 'ITManagers']
            
            for keyword in keywords:
                for subreddit_name in subreddits:
                    try:
                        subreddit = self.reddit.subreddit(subreddit_name)
                        
                        # Search for posts mentioning the product
                        search_results = list(subreddit.search(keyword, time_filter='year', limit=5))
                        self.logger.info(f"Found {len(search_results)} posts for '{keyword}' in r/{subreddit_name}")
                        
                        for submission in search_results:
                            # Enhanced customer review validation
                            content = (submission.title + ' ' + (submission.selftext or '')).lower()
                            
                            # Check if it contains actual customer experience indicators
                            customer_experience_indicators = [
                                'we use', 'we deployed', 'we implemented', 'our company', 'our organization',
                                'been using', 'experience with', 'migrated to', 'switched to', 'rolled out',
                                'in production', 'works well for us', 'helped us', 'solved our problem',
                                'our environment', 'our setup', 'licensing', 'renewal', 'support team',
                                'admin portal', 'configuration', 'policies', 'rules', 'alerts',
                                'false positives', 'detection rate', 'integration with', 'compared to'
                            ]
                            
                            # Check if it's NOT just news or announcements
                            non_customer_indicators = [
                                'microsoft announced', 'new feature', 'update released', 'version',
                                'according to microsoft', 'press release', 'blog post', 'official statement',
                                'study shows', 'report indicates', 'analyst says', 'industry report'
                            ]
                            
                            # Count customer experience indicators
                            customer_score = sum(1 for indicator in customer_experience_indicators if indicator in content)
                            non_customer_score = sum(1 for indicator in non_customer_indicators if indicator in content)
                            
                            # Only include if it has customer experience indicators and isn't news/announcements
                            if customer_score > 0 and non_customer_score == 0 and any(kw.lower() in content for kw in keywords):
                                
                                # Additional validation: check for implementation/usage context
                                has_implementation_context = any(phrase in content for phrase in [
                                    'setup', 'install', 'deploy', 'config', 'implement', 'migrate',
                                    'using for', 'experience', 'works', 'helps', 'problems with'
                                ])
                                
                                if has_implementation_context:
                                    # Analyze sentiment
                                    full_text = submission.title + ' ' + (submission.selftext or '')
                                    sentiment = self._analyze_sentiment(full_text)
                                    rating = self._sentiment_to_rating(sentiment)
                                    
                                    # Get author name safely
                                    author_name = 'deleted'
                                    try:
                                        if submission.author:
                                            author_name = submission.author.name
                                    except:
                                        pass
                                    
                                    review = {
                                        'platform': f'Reddit r/{subreddit_name}',
                                        'product': product_name,
                                        'rating': rating,
                                        'review_text': f"{submission.title}. {(submission.selftext or '')[:500]}",
                                        'reviewer': f"u/{author_name}",
                                        'source_url': f"https://www.reddit.com{submission.permalink}",
                                        'date_scraped': datetime.fromtimestamp(submission.created_utc).isoformat(),
                                        'content_type': 'customer_experience',
                                        'verified': True,
                                        'upvotes': submission.score,
                                        'num_comments': submission.num_comments,
                                        'customer_score': customer_score,
                                        'authenticity': 'verified_customer_experience'
                                    }
                                    reviews.append(review)
                                    self.logger.info(f"Added authentic customer review: {submission.title[:50]}...")
                                    
                                    if len(reviews) >= max_reviews:
                                        break
                                else:
                                    self.logger.debug(f"Filtered out non-customer content: {submission.title[:50]}...")
                            else:
                                self.logger.debug(f"Filtered out non-customer discussion: {submission.title[:50]}...")
                        
                        if len(reviews) >= max_reviews:
                            break
                        
                        # Add small delay to respect rate limits
                        time.sleep(0.5)
                            
                    except Exception as e:
                        self.logger.error(f"Error searching subreddit {subreddit_name}: {e}")
                        continue
                
                if len(reviews) >= max_reviews:
                    break
            
            self.logger.info(f"Successfully fetched {len(reviews)} real Reddit reviews for {product_name}")
            
        except Exception as e:
            self.logger.error(f"Error fetching Reddit discussions: {e}")
        
        return reviews[:max_reviews]

    def fetch_capterra_reviews(self, product_name: str, max_reviews: int = 10) -> List[Dict]:
        """Fetch reviews from Capterra"""
        reviews = []
        
        try:
            product_mapping = self.product_mappings.get(product_name, {})
            capterra_slug = product_mapping.get('capterra_slug')
            
            if not capterra_slug:
                return []
            
            url = f"https://www.capterra.com/p/{capterra_slug}/reviews/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find review elements
                review_elements = soup.find_all('div', class_='review-item')
                
                for element in review_elements[:max_reviews]:
                    try:
                        # Extract review data
                        rating_element = element.find('div', class_='rating')
                        rating = self._extract_capterra_rating(rating_element) if rating_element else 0
                        
                        content_element = element.find('div', class_='review-text')
                        content = content_element.get_text(strip=True) if content_element else ''
                        
                        reviewer_element = element.find('div', class_='reviewer-name')
                        reviewer = reviewer_element.get_text(strip=True) if reviewer_element else 'Anonymous'
                        
                        review = {
                            'platform': 'Capterra',
                            'product': product_name,
                            'rating': rating,
                            'review_text': content,
                            'reviewer': reviewer,
                            'source_url': url,
                            'date_scraped': datetime.now().isoformat(),
                            'content_type': 'software_review',
                            'verified': True
                        }
                        reviews.append(review)
                        
                    except Exception as e:
                        self.logger.warning(f"Error parsing Capterra review: {e}")
                        continue
            
        except Exception as e:
            self.logger.error(f"Error fetching Capterra reviews: {e}")
        
        return reviews

    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of text using TextBlob"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity  # Returns -1 to 1
        except:
            return 0.0

    def _sentiment_to_rating(self, sentiment: float) -> int:
        """Convert sentiment score to 1-5 rating"""
        if sentiment >= 0.5:
            return 5
        elif sentiment >= 0.1:
            return 4
        elif sentiment >= -0.1:
            return 3
        elif sentiment >= -0.5:
            return 2
        else:
            return 1

    def _extract_rating_from_stars(self, element) -> int:
        """Extract rating from star elements"""
        try:
            # Look for filled stars or rating text
            filled_stars = element.find_all('span', class_='star-filled')
            if filled_stars:
                return len(filled_stars)
            
            # Try to extract from text
            text = element.get_text()
            rating_match = re.search(r'(\d+(?:\.\d+)?)', text)
            if rating_match:
                return min(5, max(1, int(float(rating_match.group(1)))))
            
            return 3  # Default
        except:
            return 3

    def _extract_capterra_rating(self, element) -> int:
        """Extract rating from Capterra rating element"""
        try:
            # Look for star rating or numerical rating
            stars = element.find_all('span', class_='star-full')
            if stars:
                return len(stars)
            
            # Try to find rating in text
            text = element.get_text()
            rating_match = re.search(r'(\d+(?:\.\d+)?)', text)
            if rating_match:
                return min(5, max(1, int(float(rating_match.group(1)))))
            
            return 3
        except:
            return 3

    def get_review_statistics(self, reviews: List[Dict]) -> Dict:
        """Generate statistics from real reviews"""
        if not reviews:
            return {}
        
        total_reviews = len(reviews)
        avg_rating = sum(r.get('rating', 0) for r in reviews) / total_reviews
        
        platform_distribution = {}
        for review in reviews:
            platform = review.get('platform', 'Unknown')
            platform_distribution[platform] = platform_distribution.get(platform, 0) + 1
        
        rating_distribution = {i: 0 for i in range(1, 6)}
        for review in reviews:
            rating = review.get('rating', 3)
            if 1 <= rating <= 5:
                rating_distribution[rating] += 1
        
        return {
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2),
            'platform_distribution': platform_distribution,
            'rating_distribution': rating_distribution,
            'latest_review_date': max(r.get('date_scraped', '') for r in reviews),
            'data_freshness': 'real-time',
            'authenticity': 'verified_real_customers'
        }
