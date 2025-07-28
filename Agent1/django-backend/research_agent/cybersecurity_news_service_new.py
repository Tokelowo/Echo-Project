"""
Cybersecurity News Service - Fetches and analyzes cybersecurity intelligence
"""
import requests
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import feedparser
import re
import socket
from urllib.parse import urljoin
import time
import os
from django.conf import settings
from .real_customer_reviews_service import RealCustomerReviewsService
from .enhanced_reviews_service import EnhancedReviewsService
from .customer_review_validator import CustomerReviewValidator

logger = logging.getLogger(__name__)

class CybersecurityNewsService:
    """Service to fetch and analyze cybersecurity news from multiple sources"""
    
    def __init__(self):
        """Initialize service with news sources configuration"""
        # Initialize both review services
        self.real_reviews_service = RealCustomerReviewsService()
        self.enhanced_reviews_service = EnhancedReviewsService()
        self.review_validator = CustomerReviewValidator()
        
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
                'website': 'thehackernews.com',
                'priority': 'high'
            },
            'security_week': {
                'name': 'SecurityWeek',
                'rss_url': 'https://www.securityweek.com/feed/',
                'website': 'https://www.securityweek.com',
                'priority': 'high'
            },
            'krebs_security': {
                'name': 'Krebs on Security',
                'rss_url': 'https://krebsonsecurity.com/feed/',
                'website': 'https://krebsonsecurity.com',
                'priority': 'medium'
            }
        }
        
        # Initialize session
        self._setup_session()
        
        # Initialize default attributes
        self.mdo_keywords = ['cybersecurity', 'security', 'threat', 'vulnerability']
    
    def _setup_session(self):
        """Set up requests session with proper headers"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Initialize MDO/email security keywords
        self.mdo_keywords = [
            'microsoft', 'office 365', 'defender', 'email security', 'phishing',
            'malware', 'ransomware', 'business email compromise', 'bec',
            'zero-day', 'threat protection', 'advanced persistent threat',
            'email threat', 'outlook', 'exchange', 'cloud security',
            'cybersecurity', 'vulnerability', 'security', 'attack', 'breach'
        ]
    
    def fetch_cybersecurity_news(self, max_articles=30):
        """Fetch latest cybersecurity news from all sources - Enhanced for comprehensive coverage"""
        all_articles = []
        
        # Try all sources for better content variety - get more per source
        for source_id, source_config in self.sources.items():
            try:
                articles = self._fetch_from_rss(source_config, max_per_source=12)  # Increased from 4 to 12
                all_articles.extend(articles)
                logger.info(f"Fetched {len(articles)} articles from {source_config['name']}")
                
                # Don't stop early - get from all sources for comprehensive coverage
                    
            except Exception as e:
                logger.error(f"Failed to fetch from {source_config['name']}: {str(e)}")
                continue
        
        if not all_articles:
            logger.warning("No articles fetched from any source")
            return []
        
        # Sort by relevance and date, but keep more articles
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
                    
                    # Only include recent articles (last 14 days instead of 7 for more content)
                    if published_date < datetime.now() - timedelta(days=14):
                        continue
                    
                    # Calculate relevance score
                    relevance_score = self._calculate_relevance(title, summary)
                      # Include more articles by lowering threshold significantly
                    if relevance_score >= 0.5:  # Much lower threshold for more content
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
        """Calculate relevance score based on MDO/email security keywords - Enhanced for more coverage"""
        text = f"{title} {summary}".lower()
        score = 0
        
        # Base score for any cybersecurity content - more generous
        if any(word in text for word in ['security', 'cyber', 'threat', 'attack', 'hack', 'breach', 'vulnerability', 'malware', 'phishing']):
            score += 2  # Increased base score
        
        # Bonus for MDO-specific keywords
        for keyword in self.mdo_keywords:
            if keyword in text:
                if keyword in ['microsoft', 'defender', 'office 365']:
                    score += 5  # Higher relevance for direct mentions
                elif keyword in ['email', 'phishing', 'malware', 'ransomware']:
                    score += 3  # High relevance for email threats
                elif keyword in ['security', 'cybersecurity', 'threat']:
                    score += 2  # Medium relevance for general security
                else:
                    score += 1  # Low relevance for other keywords
        
        return min(score, 10)  # Cap at 10
    
    def _determine_priority(self, title, summary):
        """Determine article priority based on content"""
        text = f"{title} {summary}".lower()
        
        critical_keywords = ['zero-day', 'breach', 'ransomware', 'critical vulnerability', 'emergency patch']
        high_keywords = ['malware', 'phishing', 'threat', 'attack', 'vulnerability', 'exploit']
        
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
        
        if not all_news:
            logger.warning("No news articles fetched, returning empty list")
            return []        
        # Filter for MDO-relevant articles, but also include general cybersecurity news
        mdo_news = [article for article in all_news if article['mdo_relevant'] or article['relevance_score'] >= 2.0]
        
        return mdo_news[:max_articles]
    
    def test_fetch(self):
        """Test method to verify RSS feeds are working"""
        for source_id, source_config in self.sources.items():
            try:
                logger.info(f"Testing {source_config['name']}...")
                articles = self._fetch_from_rss(source_config, max_per_source=2)
                logger.info(f"✓ {source_config['name']}: {len(articles)} articles")
                for article in articles[:1]:  # Show first article as example
                    logger.info(f"  - {article['title'][:100]}...")
            except Exception as e:
                logger.error(f"✗ {source_config['name']}: {str(e)}")
    
    def analyze_market_presence(self, articles):
        """Analyze market presence of companies from articles with enhanced intelligence"""
        companies = {
            'Microsoft Defender for Office 365': {'articles_count': 0, 'market_score': 0, 'threat_protection_mentions': 0, 'security_mentions': 0},
            'Proofpoint': {'articles_count': 0, 'market_score': 0, 'threat_protection_mentions': 0, 'security_mentions': 0},
            'Mimecast': {'articles_count': 0, 'market_score': 0, 'threat_protection_mentions': 0, 'security_mentions': 0},
            'Symantec': {'articles_count': 0, 'market_score': 0, 'threat_protection_mentions': 0, 'security_mentions': 0},
            'Cisco': {'articles_count': 0, 'market_score': 0, 'threat_protection_mentions': 0, 'security_mentions': 0},
            'Barracuda': {'articles_count': 0, 'market_score': 0, 'threat_protection_mentions': 0, 'security_mentions': 0}
        }
        
        # Enhanced keyword mapping for better vendor detection
        company_keywords = {
            'Microsoft Defender for Office 365': [
                'microsoft', 'defender', 'office 365', 'mdo', 'microsoft defender', 
                'office', 'exchange', 'outlook', 'azure', 'microsoft 365', 'm365',
                'windows defender', 'microsoft security', 'teams'
            ],
            'Proofpoint': [
                'proofpoint', 'proofpoint tap', 'targeted attack protection',
                'proofpoint essentials', 'proofpoint enterprise'
            ],
            'Mimecast': [
                'mimecast', 'mimecast atp', 'mimecast email security',
                'mimecast gateway', 'mimecast archive'
            ],
            'Symantec': [
                'symantec', 'broadcom', 'symantec email security',
                'norton', 'symantec endpoint'
            ],
            'Cisco': [
                'cisco', 'cisco security', 'cisco umbrella', 'cisco email security',
                'ironport', 'cisco advanced malware protection'
            ],
            'Barracuda': [
                'barracuda', 'barracuda email security', 'barracuda networks',
                'barracuda essentials', 'barracuda total email protection'
            ]
        }
        
        # Email security and threat context keywords
        email_security_context = [
            'email security', 'phishing', 'malware', 'ransomware', 'business email compromise',
            'bec', 'email threat', 'spam', 'email protection', 'email defense',
            'email gateway', 'message security', 'email filtering'
        ]
        
        threat_protection_context = [
            'threat protection', 'advanced threat protection', 'atp', 'threat detection',
            'threat intelligence', 'threat prevention', 'malware protection',
            'phishing protection', 'zero-day protection', 'sandbox', 'url rewriting'
        ]
        
        security_context = [
            'security', 'cybersecurity', 'information security', 'data protection',
            'endpoint security', 'network security', 'cloud security'
        ]
        
        total_articles = len(articles)
        email_related_articles = 0
        
        # Count email-related articles for context
        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
            if any(keyword in content for keyword in email_security_context):
                email_related_articles += 1
        
        # Analyze each article for vendor mentions and context
        for article in articles:
            title_content = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
            relevance_score = article.get('relevance_score', 5)
            
            # Check each company for mentions
            for company in companies.keys():
                keywords = company_keywords.get(company, [])
                direct_mention = any(keyword in title_content for keyword in keywords)
                
                if direct_mention:
                    # Direct mention - high relevance
                    companies[company]['articles_count'] += 1
                    companies[company]['market_score'] += relevance_score * 10  # Boost for direct mentions
                    
                    # Check for threat protection context
                    if any(word in title_content for word in threat_protection_context):
                        companies[company]['threat_protection_mentions'] += 2
                    
                    # Check for security context
                    if any(word in title_content for word in security_context):
                        companies[company]['security_mentions'] += 2
                        
                # Indirect relevance - email security articles are relevant to all vendors
                elif any(keyword in title_content for keyword in email_security_context):
                    # Distribute relevance among email security vendors
                    companies[company]['market_score'] += relevance_score // 2
                    
                    # Partial credit for threat protection mentions
                    if any(word in title_content for word in threat_protection_context):
                        companies[company]['threat_protection_mentions'] += 0.3
                        
                    # Partial credit for security mentions
                    if any(word in title_content for word in security_context):
                        companies[company]['security_mentions'] += 0.3
        
        # Enhanced scoring and normalization with realistic market intelligence
        for company in companies:
            # Normalize market score based on REAL mentions only
            if companies[company]['articles_count'] > 0:
                companies[company]['market_score'] = min(95, 
                    int(companies[company]['market_score'] / max(companies[company]['articles_count'], 1)))
            else:
                # NO artificial baseline scores - only real data
                companies[company]['market_score'] = 0  # Zero score for zero mentions
                
            # Only count REAL mentions - no artificial presence assignments
            # Keep the final values as they are from real analysis
            
            # Round final values - allow zero scores for zero mentions
            companies[company]['threat_protection_mentions'] = round(companies[company]['threat_protection_mentions'], 1)
            companies[company]['security_mentions'] = round(companies[company]['security_mentions'], 1)
            # No artificial minimum scores - let real data speak
        
        # Add market intelligence metadata
        companies['_market_intelligence'] = {
            'total_articles_analyzed': total_articles,
            'email_security_articles': email_related_articles,
            'analysis_methodology': 'Enhanced vendor detection with context analysis',
            'confidence_level': min(1.0, total_articles / 20.0),  # Higher confidence with more articles
            'market_coverage': f"{len([c for c in companies if companies[c]['articles_count'] > 0])} vendors detected"
        }
        
        # Convert to expected format
        market_presence = []
        for vendor, data in companies.items():
            if vendor == '_market_intelligence':
                continue
            
            market_presence.append({
                'vendor': vendor,
                'presence_score': data['market_score'] / 100.0,  # Normalize to 0-1 scale
                'mentions': data['articles_count'],
                'context_keywords': [
                    f"security_mentions_{int(data['security_mentions'])}",
                    f"threat_protection_{int(data['threat_protection_mentions'])}",
                    f"market_score_{data['market_score']}"
                ]
            })
        
        return {
            'market_presence': market_presence,
            '_market_intelligence': companies.get('_market_intelligence', {})
        }

    def analyze_technology_trends(self, articles):
        """Analyze technology trends mentioned in articles with enhanced keyword detection"""
        trends = {
            'AI/ML Detection': 0,
            'Zero Trust': 0,
            'Cloud Security': 0,
            'ATP': 0,
            'SIEM Integration': 0,
            'Phishing Protection': 0,
            'Email Security': 0,
            'Threat Intelligence': 0,
            'Ransomware Protection': 0,
            'Endpoint Security': 0
        }
        
        # Enhanced keyword mapping with more comprehensive terms
        keyword_map = {
            'AI/ML Detection': [
                'ai', 'artificial intelligence', 'machine learning', 'ml', 'neural network',
                'deep learning', 'automation', 'intelligent', 'smart detection', 'behavioral analysis'
            ],
            'Zero Trust': [
                'zero trust', 'zerotrust', 'zero-trust', 'least privilege', 'never trust',
                'verify', 'network segmentation', 'micro-segmentation'
            ],
            'Cloud Security': [
                'cloud security', 'cloud', 'saas', 'aws', 'azure', 'gcp', 'hybrid cloud',
                'multi-cloud', 'cloud-native', 'containers', 'kubernetes'
            ],
            'ATP': [
                'atp', 'advanced threat protection', 'advanced threat', 'advanced persistent',
                'apt', 'targeted attack', 'sophisticated attack'
            ],
            'SIEM Integration': [
                'siem', 'security information', 'event management', 'log analysis',
                'correlation', 'security orchestration', 'soar', 'incident response'
            ],
            'Phishing Protection': [
                'phishing', 'phish', 'spear phishing', 'whaling', 'business email compromise',
                'bec', 'email fraud', 'social engineering', 'impersonation'
            ],
            'Email Security': [
                'email security', 'email protection', 'email threat', 'email defense',
                'message security', 'mail security', 'email gateway', 'smtp security'
            ],
            'Threat Intelligence': [
                'threat intelligence', 'threat intel', 'ioc', 'indicators of compromise',
                'threat feeds', 'threat hunting', 'cyber intelligence', 'threat landscape'
            ],
            'Ransomware Protection': [
                'ransomware', 'ransom', 'encryption attack', 'file encryption',
                'crypto-malware', 'extortion', 'data recovery', 'backup'
            ],
            'Endpoint Security': [
                'endpoint', 'edr', 'endpoint detection', 'antivirus', 'anti-malware',
                'device security', 'workstation security', 'mobile security'
            ]
        }
        
        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
            
            # Count mentions for each trend category
            for trend_name, keywords in keyword_map.items():
                for keyword in keywords:
                    if keyword in content:
                        trends[trend_name] += 1
                        break  # Count each article only once per trend
                
        # Convert to expected format
        technology_trends = []
        for trend_name, count in trends.items():
            if count > 0:  # Only include trends with mentions
                technology_trends.append({
                    'trend': trend_name,
                    'mentions': count,
                    'relevance_score': min(1.0, count / 5.0)  # Normalize to 0-1 scale
                })
        
        # Sort by mentions count
        technology_trends.sort(key=lambda x: x['mentions'], reverse=True)
        
        return {
            'technology_trends': technology_trends
        }

    def analyze_competitive_landscape(self, articles):
        """Analyze competitive landscape from articles with enhanced intelligence"""
        competitors = {}
        
        # Enhanced company mapping with comprehensive coverage
        company_map = {
            'microsoft': {
                'name': 'Microsoft',
                'products': ['Defender for Office 365', 'Microsoft 365', 'Azure Security'],
                'focus_areas': ['email security', 'cloud security', 'endpoint protection']
            },
            'proofpoint': {
                'name': 'Proofpoint', 
                'products': ['Email Protection', 'Targeted Attack Protection', 'TRAP'],
                'focus_areas': ['email security', 'threat protection', 'data loss prevention']
            },
            'mimecast': {
                'name': 'Mimecast',
                'products': ['Email Security', 'Email Archiving', 'Email Continuity'],
                'focus_areas': ['email security', 'archiving', 'continuity']
            },
            'symantec': {
                'name': 'Symantec',
                'products': ['Email Security', 'Endpoint Protection', 'Web Security'],
                'focus_areas': ['email security', 'endpoint protection', 'web security']
            },
            'cisco': {
                'name': 'Cisco',
                'products': ['Email Security', 'Umbrella', 'Advanced Malware Protection'],
                'focus_areas': ['email security', 'dns security', 'malware protection']
            },
            'barracuda': {
                'name': 'Barracuda',
                'products': ['Email Security Gateway', 'Email Protection', 'Backup'],
                'focus_areas': ['email security', 'backup', 'network security']
            },
            'forcepoint': {
                'name': 'Forcepoint',
                'products': ['Email Security', 'Data Loss Prevention', 'Web Security'],
                'focus_areas': ['email security', 'dlp', 'web security']
            },
            'trend micro': {
                'name': 'Trend Micro',
                'products': ['Email Security', 'Deep Discovery', 'Cloud App Security'],
                'focus_areas': ['email security', 'threat detection', 'cloud security']
            }
        }
        
        # Analyze each article for competitive intelligence
        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
            
            for company_key, company_info in company_map.items():
                company_name = company_info['name']
                
                # Check for company mentions (direct or product-related)
                mentioned = False
                mention_context = []
                
                # Direct company name mention
                if company_key in content:
                    mentioned = True
                    mention_context.append('direct_mention')
                
                # Product mentions
                for product in company_info['products']:
                    if product.lower() in content:
                        mentioned = True
                        mention_context.append(f'product_{product.replace(" ", "_").lower()}')
                
                # Context-based relevance (threats relevant to their focus areas)
                relevance_score = 0
                for focus_area in company_info['focus_areas']:
                    if focus_area.replace(' ', '') in content.replace(' ', ''):
                        relevance_score += 1
                        mention_context.append(f'focus_{focus_area.replace(" ", "_")}')
                
                if mentioned or relevance_score > 0:
                    if company_name not in competitors:
                        competitors[company_name] = {
                            'articles': [],
                            'total_mentions': 0,
                            'direct_mentions': 0,
                            'product_mentions': 0,
                            'focus_area_relevance': 0,
                            'threat_context': [],
                            'market_positioning': [],
                            'competitive_advantages': [],
                            'challenges_mentioned': []
                        }
                    
                    # Add article to competitor analysis
                    article_analysis = {
                        'title': article.get('title', ''),
                        'summary': article.get('summary', '')[:300],
                        'url': article.get('url', ''),
                        'published_date': article.get('published_date', ''),
                        'relevance_score': article.get('relevance_score', 5),
                        'mention_context': mention_context,
                        'threat_relevance': self._analyze_threat_context(content),
                        'competitive_signals': self._extract_competitive_signals(content, company_key)
                    }
                    
                    competitors[company_name]['articles'].append(article_analysis)
                    competitors[company_name]['total_mentions'] += 1
                    
                    # Categorize mention types
                    if 'direct_mention' in mention_context:
                        competitors[company_name]['direct_mentions'] += 1
                    if any('product_' in ctx for ctx in mention_context):
                        competitors[company_name]['product_mentions'] += 1
                    if any('focus_' in ctx for ctx in mention_context):
                        competitors[company_name]['focus_area_relevance'] += 1
                    
                    # Extract threat context
                    threat_context = self._analyze_threat_context(content)
                    if threat_context:
                        competitors[company_name]['threat_context'].extend(threat_context)
                    
                    # Extract competitive positioning signals
                    positioning = self._extract_competitive_signals(content, company_key)
                    if positioning.get('advantages'):
                        competitors[company_name]['competitive_advantages'].extend(positioning['advantages'])
                    if positioning.get('challenges'):
                        competitors[company_name]['challenges_mentioned'].extend(positioning['challenges'])
        
        # Enhance competitive analysis with market intelligence
        for company_name in competitors:
            competitor_data = competitors[company_name]
            
            # Calculate competitive strength score
            strength_score = (
                competitor_data['direct_mentions'] * 3 +
                competitor_data['product_mentions'] * 2 +
                competitor_data['focus_area_relevance'] * 1
            )
            competitor_data['competitive_strength'] = min(100, strength_score * 5)
            
            # Determine market position
            if competitor_data['direct_mentions'] > 2:
                competitor_data['market_position'] = 'Market Leader'
            elif competitor_data['total_mentions'] > 3:
                competitor_data['market_position'] = 'Strong Player'
            elif competitor_data['total_mentions'] > 1:
                competitor_data['market_position'] = 'Market Participant'
            else:
                competitor_data['market_position'] = 'Niche Player'
            
            # Clean up duplicate context items
            competitor_data['threat_context'] = list(set(competitor_data['threat_context']))[:5]
            competitor_data['competitive_advantages'] = list(set(competitor_data['competitive_advantages']))[:3]
            competitor_data['challenges_mentioned'] = list(set(competitor_data['challenges_mentioned']))[:3]
            
            # Limit articles to most relevant
            competitor_data['articles'] = sorted(
                competitor_data['articles'], 
                key=lambda x: x['relevance_score'], 
                reverse=True
            )[:5]
        
        # Add market analysis summary
        competitors['_market_analysis'] = {
            'total_competitors_detected': len(competitors) - 1,  # Exclude this summary
            'most_mentioned': max(competitors.keys(), 
                                key=lambda k: competitors[k].get('total_mentions', 0) if k != '_market_analysis' else 0,
                                default='None'),
            'competitive_intensity': 'High' if len(competitors) > 5 else 'Moderate' if len(competitors) > 3 else 'Low',
            'analysis_confidence': min(1.0, len(articles) / 15.0),
            'key_trends': self._extract_market_trends(competitors, articles)
        }
        
        # Prepare the competitive analysis data in expected format
        competitive_analysis = []
        market_trends = []
        competitive_signals = []
        
        for company_name, comp_data in competitors.items():
            if company_name == '_market_analysis':
                continue
                
            competitive_analysis.append({
                'company': company_name,
                'competitive_strength': comp_data.get('competitive_strength', 0),
                'mentions': comp_data.get('total_mentions', 0),
                'market_position': comp_data.get('market_position', 'Unknown'),
                'threat_context': comp_data.get('threat_context', []),
                'advantages': comp_data.get('competitive_advantages', []),
                'challenges': comp_data.get('challenges_mentioned', [])
            })
        
        # Extract market trends from the analysis
        if '_market_analysis' in competitors:
            market_trends = competitors['_market_analysis'].get('key_trends', [])
        
        # Extract competitive signals
        for comp_data in competitors.values():
            if isinstance(comp_data, dict):
                competitive_signals.extend(comp_data.get('competitive_advantages', []))
        
        return {
            'competitive_analysis': competitive_analysis,
            'market_trends': market_trends,
            'competitive_signals': list(set(competitive_signals))
        }
    
    def _analyze_threat_context(self, content):
        """Extract threat context from article content"""
        threat_indicators = {
            'phishing': ['phishing', 'spear phishing', 'whaling', 'email fraud'],
            'malware': ['malware', 'trojan', 'virus', 'backdoor', 'payload'],
            'ransomware': ['ransomware', 'crypto-malware', 'encryption attack'],
            'apt': ['apt', 'advanced persistent threat', 'targeted attack'],
            'bec': ['business email compromise', 'bec', 'ceo fraud'],
            'zero_day': ['zero-day', 'zero day', '0-day', 'unknown vulnerability']
        }
        
        threats_found = []
        for threat_type, indicators in threat_indicators.items():
            if any(indicator in content for indicator in indicators):
                threats_found.append(threat_type)
        
        return threats_found
    
    def _extract_competitive_signals(self, content, company):
        """Extract competitive positioning signals from content"""
        positive_signals = [
            'leader', 'leading', 'best', 'top', 'innovative', 'advanced',
            'comprehensive', 'effective', 'robust', 'reliable', 'strong'
        ]
        
        negative_signals = [
            'vulnerability', 'breach', 'failure', 'weakness', 'challenge',
            'criticism', 'issue', 'problem', 'limitation', 'concern'
        ]
        
        advantages = []
        challenges = []
        
        # Look for positive mentions
        for signal in positive_signals:
            if signal in content and company in content:
                advantages.append(signal)
        
        # Look for challenges or negative mentions
        for signal in negative_signals:
            if signal in content and company in content:
                challenges.append(signal)
        
        return {'advantages': advantages, 'challenges': challenges}
    
    def _extract_market_trends(self, competitors, articles):
        """Extract key market trends from competitive analysis"""
        trends = []
        
        # Analyze dominant themes
        all_threat_contexts = []
        for comp_name, comp_data in competitors.items():
            if comp_name != '_market_analysis':
                all_threat_contexts.extend(comp_data.get('threat_context', []))
        
        # Find most common threats
        from collections import Counter
        threat_counts = Counter(all_threat_contexts)
        top_threats = threat_counts.most_common(3)
        
        for threat, count in top_threats:
            trends.append(f"{threat.replace('_', ' ').title()} threats driving market competition")
        
        # Analyze technology focus
        tech_keywords = ['ai', 'machine learning', 'cloud', 'zero trust', 'automation']
        tech_mentions = sum(1 for article in articles 
                          for keyword in tech_keywords 
                          if keyword in (article.get('title', '') + ' ' + article.get('summary', '')).lower())
        
        if tech_mentions > len(articles) // 3:
            trends.append("Technology innovation accelerating competitive differentiation")
        
        return trends[:4]  # Limit to top 4 trends

    def analyze_threat_landscape(self, articles):
        """Analyze threat landscape from articles"""
        threats = {
            'Phishing': 0,
            'Malware': 0,
            'Ransomware': 0,
            'Advanced Persistent Threats': 0,
            'Business Email Compromise': 0,
            'Social Engineering': 0
        }
        
        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
            
            if any(word in content for word in ['phishing', 'phish']):
                threats['Phishing'] += 1
            if any(word in content for word in ['malware', 'virus', 'trojan']):
                threats['Malware'] += 1
            if any(word in content for word in ['ransomware', 'crypto']):
                threats['Ransomware'] += 1
            if any(word in content for word in ['apt', 'advanced persistent', 'targeted attack']):
                threats['Advanced Persistent Threats'] += 1
            if any(word in content for word in ['bec', 'business email compromise']):
                threats['Business Email Compromise'] += 1
            if any(word in content for word in ['social engineering', 'social']):
                threats['Social Engineering'] += 1
                
        # Convert to expected format
        threat_analysis = []
        for threat_category, count in threats.items():
            if count > 0:  # Only include threats with mentions
                threat_analysis.append({
                    'category': threat_category,
                    'mentions': count,
                    'severity_score': min(1.0, count / 3.0)  # Normalize to 0-1 scale
                })
        
        # Sort by mentions count
        threat_analysis.sort(key=lambda x: x['mentions'], reverse=True)
        
        return {
            'threat_analysis': threat_analysis
        }

    def analyze_vendor_mentions(self, articles):
        """Analyze vendor mentions in articles"""
        vendors = {}
        
        vendor_list = ['Microsoft', 'Proofpoint', 'Mimecast', 'Symantec', 'Forcepoint', 'Barracuda', 'Cisco', 'Trend Micro']
        
        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
            
            for vendor in vendor_list:
                if vendor.lower() in content:
                    if vendor not in vendors:
                        vendors[vendor] = {'mentions': 0, 'articles': []}
                    vendors[vendor]['mentions'] += 1
                    vendors[vendor]['articles'].append({
                        'title': article.get('title', ''),
                        'url': article.get('url', ''),
                        'date': article.get('published_date', '')
                    })
        
        return vendors

    def analyze_customer_sentiment(self, articles):
        """Analyze customer sentiment and reviews from news sources and articles"""
        sentiment_analysis = {
            'Microsoft Defender for Office 365': {
                'positive_mentions': 0,
                'negative_mentions': 0,
                'neutral_mentions': 0,
                'common_issues': [],
                'positive_feedback': [],
                'customer_reviews': []
            },
            'competitors': {
                'Proofpoint': {'positive': 0, 'negative': 0, 'neutral': 0},
                'Mimecast': {'positive': 0, 'negative': 0, 'neutral': 0},
                'Symantec': {'positive': 0, 'negative': 0, 'neutral': 0}
            },
            'overall_sentiment_score': 0.0,
            'real_customer_reviews': [],
            'competitor_reviews': {},
            'data_sources': ['News Articles']
        }
        
        # First, try to fetch real customer reviews
        try:
            logger.info("Fetching real customer reviews for sentiment analysis...")
            real_reviews = self.fetch_real_customer_reviews('Microsoft Defender for Office 365', max_reviews=15)
            
            if real_reviews:
                sentiment_analysis['real_customer_reviews'] = real_reviews
                sentiment_analysis['data_sources'].extend(['G2', 'TrustRadius', 'Reddit'])
                logger.info(f"Added {len(real_reviews)} real customer reviews to sentiment analysis")
            else:
                logger.warning("No real customer reviews found for sentiment analysis")
                
        except Exception as e:
            logger.error(f"Error fetching real customer reviews for sentiment: {e}")
            
        # Try to fetch competitor reviews
        try:
            competitor_reviews = {}
            for competitor in ['Proofpoint', 'Mimecast']:
                try:
                    comp_reviews = self.fetch_real_customer_reviews(competitor, max_reviews=5)
                    competitor_reviews[competitor] = comp_reviews
                except Exception as e:
                    logger.warning(f"Could not fetch {competitor} reviews: {e}")
                    competitor_reviews[competitor] = []
            
            sentiment_analysis['competitor_reviews'] = competitor_reviews
            
        except Exception as e:
            logger.error(f"Error fetching competitor reviews: {e}")
            sentiment_analysis['competitor_reviews'] = {}
        
        positive_keywords = [
            'excellent', 'great', 'amazing', 'love', 'recommend', 'best',
            'fantastic', 'works well', 'impressed', 'satisfied', 'perfect',
            'reliable', 'effective', 'easy to use', 'user friendly'
        ]
        
        negative_keywords = [
            'terrible', 'awful', 'hate', 'worst', 'disappointed', 'frustrated',
            'broken', 'useless', 'problem', 'issue', 'bug', 'difficult',
            'complicated', 'slow', 'expensive', 'not worth', 'regret'
        ]
        
        issue_keywords = [
            'false positive', 'false negative', 'performance issue', 'slow',
            'expensive', 'complex setup', 'integration problem', 'support issue',
            'licensing cost', 'deployment challenge', 'user experience'
        ]
        
        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
            
            # Check for Microsoft Defender mentions
            if any(keyword in content for keyword in ['microsoft', 'defender', 'office 365', 'mdo']):
                # Sentiment analysis
                positive_score = sum(1 for keyword in positive_keywords if keyword in content)
                negative_score = sum(1 for keyword in negative_keywords if keyword in content)
                
                if positive_score > negative_score:
                    sentiment_analysis['Microsoft Defender for Office 365']['positive_mentions'] += 1
                elif negative_score > positive_score:
                    sentiment_analysis['Microsoft Defender for Office 365']['negative_mentions'] += 1
                else:
                    sentiment_analysis['Microsoft Defender for Office 365']['neutral_mentions'] += 1
                
                # Track common issues
                for issue in issue_keywords:
                    if issue in content and issue not in sentiment_analysis['Microsoft Defender for Office 365']['common_issues']:
                        sentiment_analysis['Microsoft Defender for Office 365']['common_issues'].append(issue)
                
                # Track positive feedback themes
                if positive_score > 0:
                    for keyword in positive_keywords:
                        if keyword in content and keyword not in sentiment_analysis['Microsoft Defender for Office 365']['positive_feedback']:
                            sentiment_analysis['Microsoft Defender for Office 365']['positive_feedback'].append(keyword)
                
                # Add to customer reviews for significant sentiment
                if positive_score > 0 or negative_score > 0:
                    sentiment_analysis['Microsoft Defender for Office 365']['customer_reviews'].append({
                        'title': article.get('title', ''),
                        'sentiment': 'positive' if positive_score > negative_score else 'negative',
                        'source': article.get('source', ''),
                        'url': article.get('url', '')
                    })
            
            # Check competitors
            for competitor in sentiment_analysis['competitors']:
                if competitor.lower() in content:
                    positive_score = sum(1 for keyword in positive_keywords if keyword in content)
                    negative_score = sum(1 for keyword in negative_keywords if keyword in content)
                    
                    if positive_score > negative_score:
                        sentiment_analysis['competitors'][competitor]['positive'] += 1
                    elif negative_score > positive_score:
                        sentiment_analysis['competitors'][competitor]['negative'] += 1
                    else:
                        sentiment_analysis['competitors'][competitor]['neutral'] += 1
        
        # Calculate overall sentiment score for Microsoft Defender with transparency
        mdo_data = sentiment_analysis['Microsoft Defender for Office 365']
        total_mentions = mdo_data['positive_mentions'] + mdo_data['negative_mentions'] + mdo_data['neutral_mentions']
        
        if total_mentions > 0:
            sentiment_analysis['overall_sentiment_score'] = (
                (mdo_data['positive_mentions'] * 1.0 + mdo_data['neutral_mentions'] * 0.5) / total_mentions
            )
            sentiment_analysis['sentiment_reliability'] = {
                'total_mentions_found': total_mentions,
                'confidence_level': min(1.0, total_mentions / 10.0),  # Higher confidence with more mentions
                'data_source': 'Cybersecurity news articles (not customer reviews)',
                'methodology': 'Keyword-based sentiment analysis of news articles mentioning Microsoft Defender'
            }
        else:
            sentiment_analysis['overall_sentiment_score'] = 0.5  # Neutral default
            sentiment_analysis['sentiment_reliability'] = {
                'total_mentions_found': 0,
                'confidence_level': 0.0,
                'data_source': 'No mentions found in current article set',
                'methodology': 'Default neutral score due to lack of mentions'
            }
        
        # Add transparency notes
        sentiment_analysis['data_limitations'] = {
            'note': 'This sentiment analysis is based on news articles, not direct customer reviews',
            'limitations': [
                'News articles may not reflect actual customer satisfaction',
                'Keyword-based analysis may miss context and nuance',
                'Limited sample size from current news cycle',
                'Professional reviews differ from customer experiences'
            ],
            'recommendations': 'For accurate customer sentiment, integrate with platforms like Gartner Peer Insights, TrustRadius, or G2 Crowd'
        }
        
        # Limit lists to most relevant items and add disclaimers
        sentiment_analysis['Microsoft Defender for Office 365']['common_issues'] = sentiment_analysis['Microsoft Defender for Office 365']['common_issues'][:5]
        sentiment_analysis['Microsoft Defender for Office 365']['positive_feedback'] = sentiment_analysis['Microsoft Defender for Office 365']['positive_feedback'][:5]
        
        return sentiment_analysis

    def get_customer_insights(self, max_articles=30):
        """Get customer insights including Reddit data and sentiment analysis"""
        try:
            # Fetch articles including Reddit posts
            articles = self.fetch_cybersecurity_news(max_articles=max_articles)
            
            # Filter for customer-relevant content
            customer_content = [
                article for article in articles 
                if article.get('content_type') == 'reddit_post' or
                any(keyword in article.get('title', '').lower() + ' ' + article.get('summary', '').lower() 
                    for keyword in ['review', 'experience', 'customer', 'user', 'feedback', 'opinion'])
            ]
            
            # Analyze customer sentiment
            sentiment_analysis = self.analyze_customer_sentiment(customer_content)
            
            # Generate key insights
            key_insights = []
            mdo_data = sentiment_analysis['Microsoft Defender for Office 365']
            
            if mdo_data['positive_mentions'] > mdo_data['negative_mentions']:
                key_insights.append("Overall positive customer sentiment towards Microsoft Defender for Office 365")
            elif mdo_data['negative_mentions'] > mdo_data['positive_mentions']:
                key_insights.append("Mixed customer sentiment with some concerns about Microsoft Defender for Office 365")
            
            if mdo_data['common_issues']:
                key_insights.append(f"Common customer concerns: {', '.join(mdo_data['common_issues'][:3])}")
            
            if mdo_data['positive_feedback']:
                key_insights.append(f"Positive customer feedback: {', '.join(mdo_data['positive_feedback'][:3])}")
            
            return {
                'total_reviews': len(customer_content),
                'reddit_posts': len([a for a in customer_content if a.get('content_type') == 'reddit_post']),
                'sentiment_analysis': sentiment_analysis,
                'key_insights': key_insights,
                'customer_content': customer_content[:10],  # Sample of customer content
                'recommendation': self._generate_customer_recommendation(sentiment_analysis)
            }
        except Exception as e:
            logger.error(f"Error getting customer insights: {str(e)}")
            return {
                'total_reviews': 0,
                'reddit_posts': 0,
                'sentiment_analysis': {},
                'key_insights': ['Unable to fetch customer insights due to data source limitations'],
                'customer_content': [],
                'recommendation': 'Monitor customer feedback channels for insights'
            }

    def _generate_customer_recommendation(self, sentiment_analysis):
        """Generate recommendations based on customer sentiment analysis"""
        mdo_data = sentiment_analysis.get('Microsoft Defender for Office 365', {})
        sentiment_score = sentiment_analysis.get('overall_sentiment_score', 0.5)
        
        if sentiment_score > 0.7:
            return "Strong positive customer sentiment. Continue current strategy and leverage customer advocacy."
        elif sentiment_score > 0.5:
            return "Generally positive sentiment with room for improvement. Address common customer concerns."
        elif sentiment_score > 0.3:
            return "Mixed customer sentiment. Focus on addressing key issues and improving customer experience."
        else:
            return "Customer concerns detected. Prioritize addressing negative feedback and improving product satisfaction."
    
    def _setup_reddit_auth(self):
        """Set up Reddit OAuth authentication"""
        try:
            auth_url = 'https://www.reddit.com/api/v1/access_token'
            auth_data = {
                'grant_type': 'client_credentials'
            }
            
            # Set up authentication headers
            auth_headers = {
                'User-Agent': self.reddit_user_agent
            }
            
            # Get access token
            response = requests.post(
                auth_url,
                data=auth_data,
                headers=auth_headers,
                auth=(self.reddit_client_id, self.reddit_client_secret),
                timeout=10
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.reddit_access_token = token_data.get('access_token')
                self.reddit_token_type = token_data.get('token_type', 'bearer')
                
                # Update session headers with authentication
                self.session.headers.update({
                    'Authorization': f'{self.reddit_token_type} {self.reddit_access_token}',
                    'User-Agent': self.reddit_user_agent
                })
                
                logger.info("Reddit authentication successful")
                return True
            else:
                logger.error(f"Reddit authentication failed: {response.status_code}")
                self.reddit_authenticated = False
                return False
                
        except Exception as e:
            logger.error(f"Reddit authentication error: {str(e)}")
            self.reddit_authenticated = False
            return False

    def fetch_real_customer_reviews(self, product_name, max_reviews=20):
        """Fetch ONLY real customer experiences from authentic review platforms and discussion sites"""
        try:
            # Try primary real reviews service first (Reddit API + web scraping)
            real_reviews = self.real_reviews_service.fetch_all_real_reviews(product_name, max_reviews)
            
            if real_reviews:
                # Filter out any system notices and only return verified real reviews
                verified_reviews = [r for r in real_reviews if r.get('verified', False) and r.get('content_type') != 'system_notice']
                
                # Use validator to ensure these are actually customer reviews, not news
                authentic_reviews = self.review_validator.filter_customer_reviews(verified_reviews)
                
                if authentic_reviews:
                    logger.info(f"Successfully fetched {len(authentic_reviews)} authentic customer reviews for {product_name}")
                    return authentic_reviews
            
            # Fallback to enhanced reviews service (RSS feeds, GitHub, etc.)
            logger.info(f"Primary service found no reviews, trying enhanced service for {product_name}")
            enhanced_reviews = self.enhanced_reviews_service.fetch_daily_reviews(product_name, max_reviews)
            
            if enhanced_reviews:
                # Filter out system notices from enhanced reviews too
                verified_enhanced = [r for r in enhanced_reviews if r.get('content_type') != 'system_notice']
                
                # Validate enhanced reviews are also real customer reviews
                authentic_enhanced = self.review_validator.filter_customer_reviews(verified_enhanced)
                
                if authentic_enhanced:
                    logger.info(f"Successfully fetched {len(authentic_enhanced)} authentic reviews from enhanced service for {product_name}")
                    return authentic_enhanced
            
            # Return empty list if no real reviews are available - no simulated data
            logger.warning(f"No authentic customer reviews found for {product_name} - returning empty list")
            return []
                
        except Exception as e:
            logger.error(f"Error fetching real customer reviews: {str(e)}")
            # Return empty list - no fallback to demo data
            return []


    
    def _analyze_text_sentiment(self, text):
        """Analyze sentiment of text content"""
        positive_indicators = [
            'excellent', 'great', 'amazing', 'love', 'recommend', 'best', 'fantastic', 
            'works well', 'impressed', 'satisfied', 'perfect', 'reliable', 'effective',
            'easy', 'user friendly', 'solid', 'good', 'happy', 'pleased', 'success'
        ]
        
        negative_indicators = [
            'terrible', 'awful', 'hate', 'worst', 'disappointed', 'frustrated', 'broken',
            'useless', 'problem', 'issue', 'bug', 'difficult', 'complicated', 'slow',
            'expensive', 'not worth', 'regret', 'fail', 'poor', 'bad', 'annoying'
        ]
        
        positive_score = sum(1 for indicator in positive_indicators if indicator in text)
        negative_score = sum(1 for indicator in negative_indicators if indicator in text)
        
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'
    
    def _sentiment_to_rating(self, sentiment, score=0):
        """Convert sentiment to a 1-5 rating scale"""
        if sentiment == 'positive':
            return 4 if score < 10 else 5
        elif sentiment == 'negative':
            return 2 if score < 5 else 1
        else:
            return 3
    
    def _extract_forum_name(self, url):
        """Extract forum name from URL"""
        if 'spiceworks' in url:
            return 'Spiceworks Community'
        elif 'serverfault' in url:
            return 'Server Fault'
        elif 'experts-exchange' in url:
            return 'Experts Exchange'
        elif 'technet.microsoft' in url:
            return 'Microsoft TechNet'
        else:
            return 'IT Forum'
    
    def _extract_blog_name(self, url):
        """Extract blog name from URL"""
        if 'krebsonsecurity' in url:
            return 'Krebs on Security'
        elif 'darkreading' in url:
            return 'Dark Reading'
        elif 'csoonline' in url:
            return 'CSO Online'
        elif 'helpnetsecurity' in url:
            return 'Help Net Security'
        else:
            return 'Security Blog'
    
    def _fetch_g2_reviews(self, product_name, max_reviews=5):
        """Fetch reviews from G2.com (public data)"""
        reviews = []
        
        # G2 search URLs for email security products
        g2_search_urls = {
            'Microsoft Defender for Office 365': 'https://www.g2.com/products/microsoft-defender-for-office-365/reviews',
            'Proofpoint': 'https://www.g2.com/products/proofpoint-email-protection/reviews',
            'Mimecast': 'https://www.g2.com/products/mimecast-email-security/reviews'
        }
        
        search_url = g2_search_urls.get(product_name)
        if not search_url:
            return reviews
        
        try:
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse G2 review structure (simplified)
                review_cards = soup.find_all('div', class_=['paper', 'review-item'])[:max_reviews]
                
                for card in review_cards:
                    try:
                        # Extract review text
                        review_text_elem = card.find('div', class_=['review-text', 'expandable-text'])
                        review_text = review_text_elem.get_text(strip=True) if review_text_elem else ''
                        
                        # Extract rating
                        rating_elem = card.find('div', class_=['stars', 'rating'])
                        rating = 0
                        if rating_elem:
                            stars = rating_elem.find_all('div', class_='star')
                            rating = len([s for s in stars if 'filled' in s.get('class', [])])
                        
                        # Extract reviewer info
                        reviewer_elem = card.find('div', class_=['reviewer', 'user-info'])
                        reviewer = reviewer_elem.get_text(strip=True) if reviewer_elem else 'Anonymous'
                        
                        if review_text:
                            reviews.append({
                                'platform': 'G2',
                                'product': product_name,
                                'rating': rating,
                                'review_text': review_text[:500],  # Limit text length
                                'reviewer': reviewer,
                                'source_url': search_url,
                                'date_scraped': datetime.now().isoformat()
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing G2 review: {str(e)}")
                        continue
                        
        except Exception as e:
            logger.warning(f"Error fetching G2 reviews: {str(e)}")
        
        return reviews
    
    def _fetch_trustradius_reviews(self, product_name, max_reviews=5):
        """Fetch reviews from TrustRadius (public data)"""
        reviews = []
        
        # TrustRadius search for email security
        trustradius_urls = {
            'Microsoft Defender for Office 365': 'https://www.trustradius.com/products/microsoft-defender-for-office-365/reviews',
            'Proofpoint': 'https://www.trustradius.com/products/proofpoint-email-protection/reviews',
            'Mimecast': 'https://www.trustradius.com/products/mimecast-email-security/reviews'
        }
        
        search_url = trustradius_urls.get(product_name)
        if not search_url:
            return reviews
        
        try:
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse TrustRadius review structure
                review_items = soup.find_all('div', class_=['review-item', 'review-card'])[:max_reviews]
                
                for item in review_items:
                    try:
                        # Extract review content
                        content_elem = item.find('div', class_=['review-content', 'review-text'])
                        content = content_elem.get_text(strip=True) if content_elem else ''
                        
                        # Extract rating
                        rating_elem = item.find('div', class_=['rating', 'stars'])
                        rating = 0
                        if rating_elem:
                            rating_text = rating_elem.get_text(strip=True)
                            rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                            if rating_match:
                                rating = float(rating_match.group(1))
                        
                        # Extract reviewer
                        reviewer_elem = item.find('div', class_=['reviewer-name', 'user-name'])
                        reviewer = reviewer_elem.get_text(strip=True) if reviewer_elem else 'TrustRadius User'
                        
                        if content:
                            reviews.append({
                                'platform': 'TrustRadius',
                                'product': product_name,
                                'rating': rating,
                                'review_text': content[:500],
                                'reviewer': reviewer,
                                'source_url': search_url,
                                'date_scraped': datetime.now().isoformat()
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing TrustRadius review: {str(e)}")
                        continue
                        
        except Exception as e:
            logger.warning(f"Error fetching TrustRadius reviews: {str(e)}")
        
        return reviews
    
    def _fetch_capterra_reviews(self, product_name, max_reviews=5):
        """Fetch reviews from Capterra (public data)"""
        reviews = []
        
        # Capterra URLs for email security
        capterra_urls = {
            'Microsoft Defender for Office 365': 'https://www.capterra.com/p/166478/Microsoft-Defender-for-Office-365/',
            'Proofpoint': 'https://www.capterra.com/p/144174/Proofpoint-Email-Protection/',
            'Mimecast': 'https://www.capterra.com/p/144032/Mimecast-Email-Security/'
        }
        
        search_url = capterra_urls.get(product_name)
        if not search_url:
            return reviews
        
        try:
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse Capterra review structure
                review_blocks = soup.find_all('div', class_=['review', 'review-block'])[:max_reviews]
                
                for block in review_blocks:
                    try:
                        # Extract review text
                        text_elem = block.find('div', class_=['review-text', 'review-content'])
                        text = text_elem.get_text(strip=True) if text_elem else ''
                        
                        # Extract rating
                        rating_elem = block.find('div', class_=['rating', 'star-rating'])
                        rating = 0
                        if rating_elem:
                            stars = rating_elem.find_all('span', class_='star')
                            rating = len([s for s in stars if 'filled' in s.get('class', [])])
                        
                        # Extract reviewer
                        reviewer_elem = block.find('div', class_=['reviewer', 'review-author'])
                        reviewer = reviewer_elem.get_text(strip=True) if reviewer_elem else 'Capterra User'
                        
                        if text:
                            reviews.append({
                                'platform': 'Capterra',
                                'product': product_name,
                                'rating': rating,
                                'review_text': text[:500],
                                'reviewer': reviewer,
                                'source_url': search_url,
                                'date_scraped': datetime.now().isoformat()
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing Capterra review: {str(e)}")
                        continue
                        
        except Exception as e:
            logger.warning(f"Error fetching Capterra reviews: {str(e)}")
        
        return reviews
    
    def _fetch_gartner_peer_insights(self, product_name, max_reviews=5):
        """Fetch reviews from Gartner Peer Insights (public data)"""
        reviews = []
        
        # Gartner Peer Insights URLs
        gartner_urls = {
            'Microsoft Defender for Office 365': 'https://www.gartner.com/reviews/market/email-security/vendor/microsoft/product/microsoft-defender-for-office-365',
            'Proofpoint': 'https://www.gartner.com/reviews/market/email-security/vendor/proofpoint',
            'Mimecast': 'https://www.gartner.com/reviews/market/email-security/vendor/mimecast'
        }
        
        search_url = gartner_urls.get(product_name)
        if not search_url:
            return reviews
        
        try:
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse Gartner review structure
                review_elements = soup.find_all('div', class_=['review-item', 'peer-review'])[:max_reviews]
                
                for element in review_elements:
                    try:
                        # Extract review content
                        content_elem = element.find('div', class_=['review-content', 'peer-insight'])
                        content = content_elem.get_text(strip=True) if content_elem else ''
                        
                        # Extract rating
                        rating_elem = element.find('div', class_=['rating', 'overall-rating'])
                        rating = 0
                        if rating_elem:
                            rating_text = rating_elem.get_text(strip=True)
                            rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                            if rating_match:
                                rating = float(rating_match.group(1))
                        
                        # Extract reviewer title/role
                        role_elem = element.find('div', class_=['reviewer-role', 'job-title'])
                        role = role_elem.get_text(strip=True) if role_elem else 'IT Professional'
                        
                        if content:
                            reviews.append({
                                'platform': 'Gartner Peer Insights',
                                'product': product_name,
                                'rating': rating,
                                'review_text': content[:500],
                                'reviewer': role,
                                'source_url': search_url,
                                'date_scraped': datetime.now().isoformat()
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing Gartner review: {str(e)}")
                        continue
                        
        except Exception as e:
            logger.warning(f"Error fetching Gartner reviews: {str(e)}")
        
        return reviews
