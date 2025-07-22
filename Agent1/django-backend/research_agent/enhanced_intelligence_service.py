"""
Enhanced Intelligence Service - Combines Internal MDO Knowledge with Real-time Web Data
Optimized for low latency and comprehensive market intelligence
"""

import logging
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache
from .web_scraping_service import WebScrapingService
from .mdo_knowledge_base import MDO_INTERNAL_KNOWLEDGE, INTERNAL_THREAT_INTELLIGENCE
import time
from typing import Dict, List, Any
import json

logger = logging.getLogger(__name__)

class EnhancedIntelligenceService:
    """
    High-performance intelligence service combining internal knowledge with web data
    """
    
    def __init__(self):
        self.web_scraper = WebScrapingService()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    async def get_comprehensive_intelligence(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get comprehensive intelligence combining internal knowledge with real-time web data
        Optimized for speed with parallel processing
        """
        cache_key = 'enhanced_intelligence_data'
        cache_timeout = 900  # 15 minutes for faster updates
        
        # Check cache first unless force refresh
        if not force_refresh:
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info("Returning cached enhanced intelligence data")
                return cached_data
        
        start_time = time.time()
        logger.info("Generating enhanced intelligence with internal knowledge + web data")
        
        try:
            # Parallel data collection
            loop = asyncio.get_event_loop()
            
            # Run web scraping in thread pool for non-blocking operation
            web_data_future = loop.run_in_executor(
                self.executor,
                self._get_web_intelligence_sync
            )
            
            # Combine with internal knowledge (instant)
            internal_data = self._get_internal_intelligence()
            
            # Wait for web data
            web_data = await web_data_future
            
            # Merge and enhance data
            enhanced_data = self._merge_intelligence_data(internal_data, web_data)
            
            # Cache the results
            cache.set(cache_key, enhanced_data, cache_timeout)
            
            processing_time = time.time() - start_time
            logger.info(f"Enhanced intelligence generated in {processing_time:.2f} seconds")
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error generating enhanced intelligence: {e}")
            # Return internal knowledge as fallback
            return self._get_internal_intelligence()
    
    def _get_web_intelligence_sync(self) -> Dict[str, Any]:
        """Synchronous wrapper for web intelligence gathering"""
        try:
            return self.web_scraper.get_comprehensive_market_intelligence()
        except Exception as e:
            logger.error(f"Web intelligence failed: {e}")
            return {
                'microsoft_news': [],
                'competitor_news': {},
                'market_trends': [],
                'summary': {'total_articles': 0}
            }
    
    def _get_internal_intelligence(self) -> Dict[str, Any]:
        """Get comprehensive internal MDO intelligence"""
        return {
            'internal_knowledge': MDO_INTERNAL_KNOWLEDGE,
            'threat_intelligence': INTERNAL_THREAT_INTELLIGENCE,
            'data_source': 'internal_knowledge_base',
            'last_updated': time.time()
        }
    
    def _merge_intelligence_data(self, internal_data: Dict, web_data: Dict) -> Dict[str, Any]:
        """Merge internal knowledge with web intelligence for comprehensive view"""
        
        enhanced_competitive_metrics = self._enhance_competitive_analysis(internal_data, web_data)
        enhanced_market_intelligence = self._enhance_market_intelligence(internal_data, web_data)
        enhanced_product_features = self._enhance_product_intelligence(internal_data, web_data)
        
        return {
            # Core intelligence data
            'microsoft_news': web_data.get('microsoft_news', []),
            'competitor_news': web_data.get('competitor_news', {}),
            'market_trends': web_data.get('market_trends', []),
            
            # Enhanced with internal knowledge
            'competitive_metrics': enhanced_competitive_metrics,
            'market_intelligence': enhanced_market_intelligence,
            'product_features': enhanced_product_features,
            
            # Internal knowledge
            'mdo_capabilities': internal_data['internal_knowledge']['core_features'],
            'recent_releases': internal_data['internal_knowledge']['recent_releases'],
            'threat_intelligence': internal_data['threat_intelligence'],
            
            # Metadata
            'data_sources': ['internal_knowledge', 'web_scraping', 'rss_feeds'],
            'intelligence_quality': 'enhanced',
            'last_updated': time.time(),
            'processing_mode': 'hybrid_intelligence'
        }
    
    def _enhance_competitive_analysis(self, internal_data: Dict, web_data: Dict) -> Dict[str, Any]:
        """Enhanced competitive analysis combining internal metrics with web intelligence"""
        
        mdo_knowledge = internal_data['internal_knowledge']
        competitors = mdo_knowledge['key_competitors']
        
        market_presence = {
            'Microsoft Defender for Office 365': {
                'articles_count': len(web_data.get('microsoft_news', [])),
                'market_score': mdo_knowledge['market_metrics']['market_share'] * 4,  # Convert to 100 scale
                'threat_protection_mentions': self._count_security_mentions(web_data.get('microsoft_news', [])),
                'internal_metrics': {
                    'customer_count': mdo_knowledge['market_metrics']['customer_count'],
                    'detection_rate': mdo_knowledge['market_metrics']['threat_detection_rate'],
                    'uptime': mdo_knowledge['market_metrics']['uptime']
                },
                'competitive_advantages': mdo_knowledge['competitive_advantages']
            }
        }
        
        # Add competitor data from web + internal knowledge
        for competitor, comp_data in competitors.items():
            competitor_news = web_data.get('competitor_news', {}).get(competitor, [])
            market_presence[competitor.title()] = {
                'articles_count': len(competitor_news),
                'market_score': comp_data['market_share'] * 4,
                'threat_protection_mentions': self._count_security_mentions(competitor_news),
                'internal_analysis': {
                    'market_share': comp_data['market_share'],
                    'strengths': comp_data['strengths'],
                    'weaknesses': comp_data['weaknesses']
                }
            }
        
        return {
            'market_presence': market_presence,
            'technology_trends': self._analyze_technology_trends(web_data, internal_data),
            'competitive_positioning': self._analyze_competitive_positioning(internal_data)
        }
    
    def _enhance_market_intelligence(self, internal_data: Dict, web_data: Dict) -> Dict[str, Any]:
        """Enhanced market intelligence with internal insights"""
        
        return {
            'market_summary': {
                'total_articles': len(web_data.get('microsoft_news', [])) + 
                               sum(len(articles) for articles in web_data.get('competitor_news', {}).values()),
                'mdo_market_share': internal_data['internal_knowledge']['market_metrics']['market_share'],
                'threat_landscape': internal_data['threat_intelligence']['latest_threats'],
                'protection_effectiveness': internal_data['threat_intelligence']['protection_effectiveness']
            },
            'recent_developments': internal_data['internal_knowledge']['recent_releases']['2025_q2'],
            'web_intelligence': web_data.get('summary', {}),
            'data_freshness': 'Real-time hybrid intelligence'
        }
    
    def _enhance_product_intelligence(self, internal_data: Dict, web_data: Dict) -> Dict[str, Any]:
        """Enhanced product intelligence with detailed feature analysis"""
        
        features = internal_data['internal_knowledge']['core_features']
        
        return {
            'Microsoft Defender for Office 365': {
                feature_name: {
                    'capability_score': feature_data.get('customer_satisfaction', 4.5) * 20,  # Convert to 100 scale
                    'market_adoption': feature_data.get('adoption_rate', 85),
                    'innovation_rate': 90 + (len(feature_data.get('capabilities', [])) * 2),
                    'internal_metrics': {
                        'release_date': feature_data.get('release_date'),
                        'latest_update': feature_data.get('latest_update'),
                        'market_advantage': feature_data.get('market_advantage'),
                        'capabilities': feature_data.get('capabilities', [])
                    }
                }
                for feature_name, feature_data in features.items()
            }
        }
    
    def _count_security_mentions(self, articles: List[Dict]) -> int:
        """Count security-related mentions in articles"""
        security_keywords = [
            'security', 'threat', 'phishing', 'malware', 'protection',
            'cybersecurity', 'breach', 'vulnerability', 'attack', 'defense'
        ]
        
        count = 0
        for article in articles:
            content = article.get('content', '').lower()
            count += sum(1 for keyword in security_keywords if keyword in content)
        
        return count
    
    def _analyze_technology_trends(self, web_data: Dict, internal_data: Dict) -> Dict[str, int]:
        """Analyze technology trends from web data and internal knowledge"""
        
        trends = {
            'Email Security': 25,
            'Threat Protection': 30,
            'Anti-Phishing': 28,
            'Advanced Threat Protection': 22,
            'Zero Trust': 35,  # High due to Microsoft's focus
            'AI-Powered Security': 40  # High due to recent AI investments
        }
        
        # Enhance with web data analysis
        all_content = ""
        for articles in web_data.get('competitor_news', {}).values():
            for article in articles:
                all_content += article.get('content', '').lower()
        
        # Adjust trends based on web mentions
        trend_keywords = {
            'Email Security': ['email security', 'email protection'],
            'Zero Trust': ['zero trust', 'zero-trust'],
            'AI-Powered Security': ['ai security', 'machine learning', 'artificial intelligence']
        }
        
        for trend, keywords in trend_keywords.items():
            mentions = sum(all_content.count(keyword) for keyword in keywords)
            trends[trend] = min(trends[trend] + mentions, 50)  # Cap at 50
        
        return trends
    
    def _analyze_competitive_positioning(self, internal_data: Dict) -> Dict[str, Any]:
        """Analyze competitive positioning based on internal knowledge"""
        
        mdo_metrics = internal_data['internal_knowledge']['market_metrics']
        competitors = internal_data['internal_knowledge']['key_competitors']
        
        return {
            'market_leadership': {
                'position': 1 if mdo_metrics['market_share'] > 20 else 2,
                'market_share': mdo_metrics['market_share'],
                'key_differentiators': list(internal_data['internal_knowledge']['competitive_advantages'].values())
            },
            'competitive_gaps': self._identify_competitive_gaps(competitors),
            'growth_opportunities': [
                'Mobile security expansion',
                'Small business market penetration',
                'Enhanced AI/ML capabilities'
            ]
        }
    
    def _identify_competitive_gaps(self, competitors: Dict) -> List[str]:
        """Identify potential competitive gaps"""
        
        all_competitor_strengths = []
        for comp_data in competitors.values():
            all_competitor_strengths.extend(comp_data['strengths'])
        
        # Areas where competitors are strong
        strength_areas = list(set(all_competitor_strengths))
        
        return [
            f"Monitor competitive advantage in: {strength}"
            for strength in strength_areas[:3]  # Top 3 areas to watch
        ]

# Global instance for reuse
enhanced_intelligence_service = EnhancedIntelligenceService()
