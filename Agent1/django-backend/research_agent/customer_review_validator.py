"""
Customer Review Validator - Ensures only real customer reviews are displayed
"""
import re
from typing import List, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CustomerReviewValidator:
    """Validates and filters customer reviews to ensure authenticity"""
    
    def __init__(self):
        # Keywords that indicate real customer reviews
        self.customer_review_indicators = [
            'purchased', 'bought', 'using for', 'deployed', 'implemented',
            'our company', 'our organization', 'we use', 'we deployed',
            'in production', 'license', 'subscription', 'support team',
            'customer success', 'renewal', 'upgrade', 'pricing',
            'features we love', 'features we need', 'works well for us',
            'recommend to', 'would not recommend', 'switched from',
            'compared to', 'migration from', 'rollout', 'training',
            'admin console', 'configuration', 'setup process',
            'our IT team', 'our security team', 'end users',
            'daily use', 'monthly cost', 'annual contract'
        ]
        
        # Keywords that indicate non-customer content (news, announcements, etc.)
        self.non_customer_indicators = [
            'announced', 'launches', 'releases', 'updates', 'version',
            'according to', 'reported by', 'study shows', 'research indicates',
            'analyst says', 'expert opinion', 'industry report',
            'press release', 'official statement', 'spokesperson',
            'market research', 'survey results', 'whitepaper',
            'blog post', 'article', 'news report', 'breaking news',
            'gartner says', 'forrester', 'idc report', 'vendor claims',
            'partnership', 'acquisition', 'merger', 'ipo',
            'conference', 'presentation', 'webinar', 'demo',
            'promotional', 'marketing', 'advertisement', 'sponsored'
        ]
        
        # Trusted review platforms
        self.trusted_platforms = [
            'g2', 'trustradius', 'capterra', 'gartner peer insights',
            'software advice', 'getapp', 'reddit r/sysadmin',
            'reddit r/cybersecurity', 'reddit r/office365',
            'reddit r/security', 'reddit r/itmanagers',
            'spiceworks community', 'technet', 'stack overflow',
            'user forums', 'customer community', 'support forums'
        ]
        
        # Minimum review quality thresholds
        self.min_review_length = 50  # Minimum characters for a meaningful review
        self.min_rating_context = 20  # Minimum characters when rating is provided
        
    def validate_customer_review(self, review: Dict[str, Any]) -> bool:
        """
        Validates if a review is from a real customer vs. news/announcement
        Returns True if it's a real customer review, False otherwise
        """
        try:
            # Check if it's marked as a system notice
            if review.get('content_type') == 'system_notice':
                return False
            
            # Get review content
            content = review.get('review_text', '') or review.get('content', '') or ''
            title = review.get('title', '')
            platform = review.get('platform', '').lower()
            
            if not content:
                return False
                
            # Combine title and content for analysis
            full_text = f"{title} {content}".lower()
            
            # Check minimum length requirements
            if len(content) < self.min_review_length:
                if review.get('rating') and len(content) < self.min_rating_context:
                    return False
            
            # Check if from trusted review platform
            platform_trusted = any(trusted in platform for trusted in self.trusted_platforms)
            
            # Count customer review indicators
            customer_indicators = sum(1 for indicator in self.customer_review_indicators 
                                    if indicator in full_text)
            
            # Count non-customer indicators
            non_customer_indicators = sum(1 for indicator in self.non_customer_indicators 
                                        if indicator in full_text)
            
            # Additional checks for authentic customer reviews
            has_specific_experience = any(phrase in full_text for phrase in [
                'we have been using', 'after using', 'been using for',
                'our experience with', 'in our environment', 'for our business',
                'works great for us', 'solved our problem', 'helped us',
                'our team loves', 'our team struggles', 'integration with our',
                'compared to our previous', 'since we switched'
            ])
            
            has_implementation_details = any(phrase in full_text for phrase in [
                'setup was', 'configuration', 'deployment took', 'rollout',
                'training was', 'support helped', 'installation',
                'onboarding', 'migration from', 'integration with'
            ])
            
            has_specific_features = any(phrase in full_text for phrase in [
                'feature that', 'functionality', 'dashboard', 'reporting',
                'alerts', 'notifications', 'automation', 'policies',
                'rules', 'settings', 'admin panel', 'user interface'
            ])
            
            # Scoring system for authenticity
            authenticity_score = 0
            
            # Positive indicators
            if platform_trusted:
                authenticity_score += 3
            if customer_indicators > 0:
                authenticity_score += min(customer_indicators, 5)
            if has_specific_experience:
                authenticity_score += 2
            if has_implementation_details:
                authenticity_score += 2
            if has_specific_features:
                authenticity_score += 1
            if review.get('rating') is not None:
                authenticity_score += 1
            if review.get('reviewer') and review.get('reviewer') != 'Anonymous':
                authenticity_score += 1
            
            # Negative indicators
            if non_customer_indicators > 0:
                authenticity_score -= min(non_customer_indicators * 2, 8)
            
            # Check for obvious news/announcement patterns
            if any(phrase in full_text for phrase in [
                'announced today', 'press release', 'according to sources',
                'industry analyst', 'market research', 'study reveals'
            ]):
                authenticity_score -= 5
            
            # Final decision
            is_customer_review = authenticity_score >= 3
            
            # Log validation results for debugging
            logger.debug(f"Review validation: score={authenticity_score}, "
                        f"customer_indicators={customer_indicators}, "
                        f"non_customer_indicators={non_customer_indicators}, "
                        f"platform_trusted={platform_trusted}, "
                        f"is_customer_review={is_customer_review}")
            
            return is_customer_review
            
        except Exception as e:
            logger.error(f"Error validating customer review: {e}")
            return False
    
    def filter_customer_reviews(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters a list of reviews to only include authentic customer reviews
        """
        if not reviews:
            return []
        
        validated_reviews = []
        
        for review in reviews:
            if self.validate_customer_review(review):
                # Mark as validated
                review['validated'] = True
                review['validation_score'] = 'authentic_customer'
                validated_reviews.append(review)
            else:
                # Log why it was filtered out
                logger.info(f"Filtered out non-customer content: {review.get('platform', 'Unknown')} - "
                           f"{review.get('review_text', '')[:100]}...")
        
        # Sort by authenticity indicators (most authentic first)
        validated_reviews.sort(key=lambda x: (
            x.get('rating', 0),
            len(x.get('review_text', '')),
            1 if any(platform in x.get('platform', '').lower() for platform in self.trusted_platforms) else 0
        ), reverse=True)
        
        logger.info(f"Filtered {len(reviews)} reviews down to {len(validated_reviews)} authentic customer reviews")
        
        return validated_reviews
    
    def add_review_authenticity_metadata(self, review: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds metadata about review authenticity and validation
        """
        if not review:
            return review
            
        # Add validation metadata
        review['authenticity_check'] = {
            'validated_at': datetime.now().isoformat(),
            'validation_method': 'customer_review_validator',
            'is_authentic_customer': self.validate_customer_review(review),
            'platform_trusted': any(platform in review.get('platform', '').lower() 
                                   for platform in self.trusted_platforms),
            'content_length': len(review.get('review_text', '')),
            'has_rating': review.get('rating') is not None
        }
        
        return review
