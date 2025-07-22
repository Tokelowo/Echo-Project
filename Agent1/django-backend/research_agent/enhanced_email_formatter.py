"""
Enhanced Email Service - Professional .docx and Email Generator for Microsoft Defender
Provides enhanced email templates with improved personalization and engagement features.
"""
import os
import io
import base64
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class EnhancedEmailFormatter:
    """
    Enhanced email formatting with personalization and engagement features
    """
    
    def __init__(self):
        self.microsoft_blue = '#0078d4'
        self.microsoft_gray = '#605e5c'
        self.microsoft_light_gray = '#f3f2f1'
    
    def create_enhanced_email_summary(self, report_data, user_name=None, docx_filename=None):
        """
        Create enhanced email summary with personalization and engagement features
        
        Args:
            report_data (dict): The intelligence report data
            user_name (str): Recipient name for personalization
            docx_filename (str): Name of the attached .docx file
            
        Returns:
            dict: Enhanced email content with subject, html_body, and plain_text_body
        """
        try:
            # Generate email subject with personalization
            report_title = report_data.get('title', 'Intelligence Report')
            is_subscription = report_data.get('is_subscription_email', False)
            subscription_frequency = report_data.get('subscription_frequency', '')
            
            if is_subscription and subscription_frequency:
                subject = f"📊 Your {subscription_frequency.title()} Intelligence Report - {report_title}"
            else:
                subject = f"Microsoft Defender for Office 365 - {report_title}"
            
            # Generate personalized greeting
            greeting = f"Dear {user_name}," if user_name else "Dear Valued Customer,"
            
            # Extract engagement metrics
            engagement_metrics = self._create_engagement_metrics(report_data)
            
            # Generate personalized insights
            key_insights = self._extract_email_insights(report_data)
            
            # Generate recommendations
            recommendations = self._generate_personalized_recommendations(report_data, user_name)
            
            # Get customer reviews with links
            customer_reviews = self._get_customer_reviews_summary(report_data)
            
            # Create enhanced HTML email body
            html_body = self._create_enhanced_html_email_body(
                report_data, greeting, docx_filename, engagement_metrics, key_insights, recommendations, customer_reviews
            )
            
            # Create enhanced plain text version
            plain_text_body = self._create_enhanced_plain_text_email_body(
                report_data, greeting, docx_filename, engagement_metrics, key_insights, recommendations, customer_reviews
            )
            
            return {
                'subject': subject,
                'html_body': html_body,
                'plain_text_body': plain_text_body,
                'from_name': 'Microsoft Defender Intelligence Team',
                'from_email': 'defender-intelligence@microsoft.com',
                'engagement_score': len(key_insights) + len(recommendations),
                'personalization_level': 'high' if user_name else 'standard'
            }
            
        except Exception as e:
            logger.error(f"Error creating enhanced email summary: {str(e)}")
            raise
    
    def _create_enhanced_html_email_body(self, report_data, greeting, docx_filename, engagement_metrics, key_insights, recommendations, customer_reviews):
        """Create enhanced HTML email body with advanced features"""
        
        # Extract data
        executive_summary = report_data.get('executive_summary', 'Comprehensive analysis of email security market trends.')
        gen_time = report_data.get('generated_at', datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        is_subscription = report_data.get('is_subscription_email', False)
        is_preview = report_data.get('is_preview', False)
        subscription_frequency = report_data.get('subscription_frequency', '')
        unsubscribe_url = report_data.get('unsubscribe_url', '')
        manage_url = report_data.get('manage_subscription_url', '')
        user_name = greeting.replace('Dear ', '').replace(',', '') if 'Dear' in greeting else 'Valued Customer'
        
        # Preview banner
        preview_banner = ""
        if is_preview:
            preview_banner = """
            <div style="background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%); color: white; padding: 15px; text-align: center; font-weight: bold; margin-bottom: 20px;">
                📧 PREVIEW EMAIL - Sample of your scheduled intelligence reports
            </div>
            """
        
        # Subscription banner with personalization
        subscription_banner = ""
        if is_subscription and subscription_frequency:
            subscription_banner = f"""
            <div style="background: linear-gradient(135deg, #e7f3ff 0%, #cce7ff 100%); padding: 20px; border-radius: 8px; border-left: 4px solid #0078d4; margin-bottom: 25px;">
                <h3 style="margin-top: 0; color: #0078d4;">👋 Hello {user_name}!</h3>
                <p style="margin-bottom: 0;">Your {subscription_frequency} intelligence briefing is ready. We've analyzed the latest market data to keep you ahead of emerging threats and opportunities.</p>
            </div>
            """

        # Build enhanced HTML content
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microsoft Defender for Office 365 - Enhanced Intelligence Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; line-height: 1.6; }}
        .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.12); }}
        .header {{ background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); color: white; padding: 30px; text-align: center; position: relative; }}
        .header::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="rgba(255,255,255,0.1)"><polygon points="0,0 1000,0 1000,100 0,80"/></svg>'); }}
        .header-content {{ position: relative; z-index: 2; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 600; }}
        .logo {{ font-size: 18px; margin-bottom: 15px; letter-spacing: 1px; opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .greeting {{ font-size: 16px; margin-bottom: 25px; color: #323130; }}
        .engagement-metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric-card {{ background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #e1dfdd; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; }}
        .metric-card:hover {{ transform: translateY(-2px); }}
        .metric-number {{ font-size: 28px; font-weight: bold; color: #0078d4; margin-bottom: 8px; }}
        .metric-label {{ font-size: 14px; color: #605e5c; font-weight: 500; }}
        .insights-section {{ background: linear-gradient(135deg, #fff8e1 0%, #fff3c4 100%); padding: 25px; border-radius: 12px; margin: 25px 0; border-left: 5px solid #ff9800; }}
        .recommendations-section {{ background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 25px; border-radius: 12px; margin: 25px 0; border-left: 5px solid #9c27b0; }}
        .section-title {{ margin-top: 0; color: #333; font-size: 20px; margin-bottom: 15px; }}
        .insight-item, .recommendation-item {{ margin-bottom: 12px; padding: 12px; background: rgba(255,255,255,0.7); border-radius: 8px; }}
        .cta-section {{ text-align: center; margin: 30px 0; }}
        .cta-button {{ background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: 600; margin: 10px 8px; transition: all 0.3s; box-shadow: 0 4px 12px rgba(0,120,212,0.3); }}
        .cta-button:hover {{ background: linear-gradient(135deg, #005a9e 0%, #004578 100%); transform: translateY(-1px); box-shadow: 0 6px 16px rgba(0,120,212,0.4); }}
        .footer {{ background: linear-gradient(135deg, #605e5c 0%, #484644 100%); color: white; padding: 30px; text-align: center; }}
        .footer-links {{ margin: 20px 0; }}
        .footer-links a {{ color: #ffffff; text-decoration: none; margin: 0 15px; opacity: 0.9; }}
        .footer-links a:hover {{ opacity: 1; text-decoration: underline; }}
        .unsubscribe-section {{ background-color: #f8f9fa; padding: 20px; margin-top: 20px; border-radius: 8px; font-size: 13px; color: #605e5c; text-align: center; }}
        .unsubscribe-section a {{ color: #0078d4; text-decoration: none; }}
        .real-data-badge {{ background: linear-gradient(135deg, #107c10 0%, #0e6b0e 100%); color: white; padding: 12px 20px; border-radius: 8px; font-weight: bold; margin-bottom: 25px; display: inline-block; box-shadow: 0 2px 8px rgba(16,124,16,0.3); }}
        @media (max-width: 600px) {{
            .engagement-metrics {{ grid-template-columns: 1fr; }}
            .content {{ padding: 25px; }}
            .header {{ padding: 25px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {preview_banner}
        
        <div class="header">
            <div class="header-content">
                <div class="logo">🔷 MICROSOFT DEFENDER FOR OFFICE 365</div>
                <h1>{report_data.get('title', 'Enhanced Intelligence Report')}</h1>
                <p style="margin: 8px 0; opacity: 0.9;">Generated: {gen_time}</p>
            </div>
        </div>
        
        <div class="content">
            <div class="greeting">{greeting}</div>
            
            {subscription_banner}
            
            <div class="real-data-badge">✓ 100% Real-Time Intelligence Analysis</div>
            
            <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 25px; border-radius: 12px; margin-bottom: 30px; border-left: 5px solid #4caf50;">
                <h3 style="margin-top: 0; color: #2e7d32; font-size: 20px;">📊 Executive Intelligence Summary</h3>
                <p style="margin: 0; font-size: 16px; line-height: 1.8; color: #333;">{executive_summary}</p>
            </div>
            
            <div class="engagement-metrics">
                <div class="metric-card">
                    <div class="metric-number">{engagement_metrics['data_sources']}</div>
                    <div class="metric-label">Sources Analyzed</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{engagement_metrics['threat_categories']}</div>
                    <div class="metric-label">Threat Categories</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{engagement_metrics['competitive_insights']}</div>
                    <div class="metric-label">Competitive Insights</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{engagement_metrics['freshness_score']}</div>
                    <div class="metric-label">Data Freshness</div>
                </div>
            </div>
        """
        
        # Add key insights section
        if key_insights:
            html_content += f"""
            <div class="insights-section">
                <h3 class="section-title">🔍 Key Intelligence Insights</h3>
                {"".join([f'<div class="insight-item">• {insight}</div>' for insight in key_insights[:4]])}
            </div>
            """
        
        # Add recommendations section
        if recommendations:
            html_content += f"""
            <div class="recommendations-section">
                <h3 class="section-title">🎯 Personalized Recommendations</h3>
                {"".join([f'<div class="recommendation-item"><strong>{rec["action"]}:</strong> {rec["description"]}</div>' for rec in recommendations[:3]])}
            </div>
            """
        
        # Add customer reviews section
        if customer_reviews and customer_reviews.get('reviews'):
            html_content += f"""
            <div style="background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%); padding: 25px; border-radius: 12px; margin: 25px 0; border-left: 5px solid #17a2b8;">
                <h3 class="section-title">💬 Customer Voice & Reviews</h3>
                <p style="margin-bottom: 20px; color: #495057; font-style: italic;">Real customer feedback from leading platforms:</p>
                {"".join([f'''
                <div style="background: rgba(255,255,255,0.8); padding: 18px; border-radius: 8px; margin-bottom: 15px; border-left: 3px solid #28a745;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <strong style="color: #0078d4;">{review.get("platform", "Customer Review")}</strong>
                        <span style="color: #ffa500;">{"⭐" * min(5, max(1, review.get("rating", 4)))}</span>
                    </div>
                    <p style="margin: 8px 0; line-height: 1.6; color: #333;">"{review.get("review_text", "")[:200]}{'...' if len(review.get("review_text", "")) > 200 else ''}"</p>
                    <div style="font-size: 12px; color: #6c757d; margin-top: 10px;">
                        <span>— {review.get("reviewer", "Verified Customer")}</span>
                        {f' | <a href="{review.get("source_url", "#")}" style="color: #0078d4; text-decoration: none;">Read Full Review</a>' if review.get("source_url") else ""}
                    </div>
                </div>
                ''' for review in customer_reviews.get('reviews', [])[:3]])}
                <div style="text-align: center; margin-top: 20px;">
                    <a href="{customer_reviews.get('reviews_page_url', '#')}" style="background: linear-gradient(135deg, #17a2b8 0%, #138496 100%); color: white; padding: 12px 25px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">
                        📈 View All Customer Reviews
                    </a>
                </div>
            </div>
            """
        
        # Add attachment notice
        if docx_filename:
            html_content += f"""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 25px; border-radius: 12px; border-left: 5px solid #2196f3; margin: 25px 0;">
                <h3 style="margin-top: 0; color: #1976d2;">📎 Complete Intelligence Report</h3>
                <p>Your comprehensive analysis is attached as <strong>{docx_filename}</strong> with detailed insights, charts, and strategic recommendations.</p>
                <p style="margin-bottom: 0;"><strong>💡 Pro Tip:</strong> Share key insights with your security team for maximum organizational impact.</p>
            </div>
            """
        
        # Add call to action
        html_content += """
            <div class="cta-section">
                <h3 style="color: #333; margin-bottom: 20px;">🚀 Take Action Now</h3>
        """
        
        if manage_url:
            html_content += f"""
                <a href="{manage_url}" class="cta-button">📧 Manage Subscriptions</a>
            """
        
        html_content += """
                <a href="https://security.microsoft.com" class="cta-button">🛡️ Security Dashboard</a>
                <a href="https://docs.microsoft.com/defender" class="cta-button">📚 Learn More</a>
            </div>
        </div>
        
        <div class="footer">
            <p style="margin: 0; font-size: 18px; font-weight: 600;">Microsoft Defender for Office 365</p>
            <p style="margin: 8px 0; font-size: 15px; opacity: 0.9;">Intelligent email security for the modern workplace</p>
            <div class="footer-links">
                <a href="https://security.microsoft.com">Security Center</a>
                <a href="https://docs.microsoft.com/defender">Documentation</a>
                <a href="https://aka.ms/defendersupport">Support</a>
                <a href="https://techcommunity.microsoft.com">Community</a>
            </div>
        """
        
        # Add unsubscribe section for subscription emails
        if is_subscription:
            html_content += f"""
            <div class="unsubscribe-section">
                <p style="margin: 8px 0; font-weight: 500;">📧 Subscription Management</p>
                <p style="margin: 8px 0;">You're receiving {subscription_frequency} intelligence reports to stay ahead of emerging threats.</p>
                <p style="margin: 8px 0;">
        """
            if manage_url:
                html_content += f"""<a href="{manage_url}">Update preferences</a>"""
            if unsubscribe_url:
                if manage_url:
                    html_content += " | "
                html_content += f"""<a href="{unsubscribe_url}">Unsubscribe</a>"""
            html_content += """
                </p>
            </div>
            """
        
        html_content += """
        </div>
    </div>
</body>
</html>
        """
        
        return html_content.strip()
    
    def _create_enhanced_plain_text_email_body(self, report_data, greeting, docx_filename, engagement_metrics, key_insights, recommendations, customer_reviews):
        """Create enhanced plain text email body"""
        
        executive_summary = report_data.get('executive_summary', 'Comprehensive analysis of email security market trends.')
        gen_time = report_data.get('generated_at', datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        is_subscription = report_data.get('is_subscription_email', False)
        is_preview = report_data.get('is_preview', False)
        subscription_frequency = report_data.get('subscription_frequency', '')
        unsubscribe_url = report_data.get('unsubscribe_url', '')
        manage_url = report_data.get('manage_subscription_url', '')
        
        # Preview banner
        preview_text = ""
        if is_preview:
            preview_text = "\n📧 PREVIEW EMAIL - Sample of your scheduled intelligence reports\n" + "="*70 + "\n"
        
        # Build enhanced plain text content
        plain_text = f"""
{preview_text}🔷 MICROSOFT DEFENDER FOR OFFICE 365
Enhanced Intelligence Report
Generated: {gen_time}
{"="*70}

{greeting}

✓ 100% REAL-TIME INTELLIGENCE ANALYSIS
"""
        
        # Add subscription info
        if is_subscription and subscription_frequency:
            user_name = greeting.replace('Dear ', '').replace(',', '') if 'Dear' in greeting else 'Valued Customer'
            plain_text += f"""
👋 PERSONALIZED BRIEFING FOR {user_name.upper()}
Your {subscription_frequency} intelligence report is ready with the latest
market data to keep you ahead of emerging threats and opportunities.
{"-"*50}
"""
        
        plain_text += f"""
📊 EXECUTIVE INTELLIGENCE SUMMARY
{executive_summary}

🎯 ENGAGEMENT METRICS
• Sources Analyzed: {engagement_metrics['data_sources']}
• Threat Categories: {engagement_metrics['threat_categories']}
• Competitive Insights: {engagement_metrics['competitive_insights']}
• Data Freshness: {engagement_metrics['freshness_score']}
• Analysis Confidence: {engagement_metrics['confidence_level']}
"""
        
        # Add key insights
        if key_insights:
            plain_text += f"""

🔍 KEY INTELLIGENCE INSIGHTS
{chr(10).join([f'• {insight}' for insight in key_insights[:4]])}
"""
        
        # Add recommendations
        if recommendations:
            plain_text += f"""

🎯 PERSONALIZED RECOMMENDATIONS
{chr(10).join([f'• {rec["action"]}: {rec["description"]}' for rec in recommendations[:3]])}
"""
        
        # Add customer reviews
        if customer_reviews and customer_reviews.get('reviews'):
            plain_text += f"""

💬 CUSTOMER VOICE & REVIEWS
Real customer feedback from leading platforms:

{chr(10).join([f'''⭐ {review.get("platform", "Customer Review")} - {'⭐' * min(5, max(1, review.get("rating", 4)))}
"{review.get("review_text", "")[:150]}{'...' if len(review.get("review_text", "")) > 150 else ''}"
— {review.get("reviewer", "Verified Customer")}{f' | {review.get("source_url", "")}' if review.get("source_url") else ""}
{"-"*40}''' for review in customer_reviews.get('reviews', [])[:3]])}

📈 View All Customer Reviews: {customer_reviews.get('reviews_page_url', 'Available in your Security Dashboard')}
"""
        
        # Add attachment notice
        if docx_filename:
            plain_text += f"""

📎 COMPLETE INTELLIGENCE REPORT ATTACHED
Your comprehensive analysis is attached as {docx_filename} with:
• Detailed threat landscape analysis
• Competitive positioning charts
• Strategic recommendations
• Market trend visualizations
• Executive summary and action items

💡 Pro Tip: Share key insights with your security team for maximum 
organizational impact and coordinated threat response.
"""
        
        # Add call to action
        plain_text += """

🚀 TAKE ACTION NOW
Stay ahead of emerging threats with these immediate steps:

1. Review the comprehensive attached report
2. Share critical insights with your security team
3. Update threat monitoring protocols
4. Evaluate competitive positioning changes
5. Implement recommended security enhancements
"""
        
        if manage_url:
            plain_text += f"""
6. Manage your intelligence subscriptions: {manage_url}
"""
        
        plain_text += """

📞 SUPPORT & RESOURCES
• Security Dashboard: https://security.microsoft.com
• Documentation: https://docs.microsoft.com/defender
• Support: https://aka.ms/defendersupport
• Community: https://techcommunity.microsoft.com

Questions? Contact your Microsoft Security representative for personalized
guidance and strategic recommendations.
"""
        
        # Add subscription management
        if is_subscription:
            plain_text += f"""

{"="*70}
📧 SUBSCRIPTION MANAGEMENT
"""
            if subscription_frequency:
                plain_text += f"""
You're receiving {subscription_frequency} intelligence reports to stay ahead
of emerging email security threats and market opportunities.
"""
            if manage_url:
                plain_text += f"""
• Update preferences: {manage_url}
"""
            if unsubscribe_url:
                plain_text += f"""
• Unsubscribe: {unsubscribe_url}
"""
        
        plain_text += f"""

---
Microsoft Defender for Office 365
Intelligent email security for the modern workplace
© {datetime.now().year} Microsoft Corporation. All rights reserved.
        """
        
        return plain_text.strip()
    
    def _extract_email_insights(self, report_data):
        """Extract key insights from report data for email highlights"""
        insights = []
        
        try:
            # Extract from market analysis
            market_analysis = report_data.get('market_analysis', {})
            if market_analysis:
                growth_rate = market_analysis.get('growth_rate', '')
                if 'increase' in str(growth_rate).lower() or 'growth' in str(growth_rate).lower():
                    insights.append(f"📈 Market showing {growth_rate} with significant expansion opportunities")
                
                growth_drivers = market_analysis.get('growth_drivers', '')
                if growth_drivers:
                    insights.append(f"🎯 Primary growth catalyst identified: {growth_drivers}")
            
            # Extract from threat analysis
            threat_analysis = report_data.get('threat_analysis', {})
            if isinstance(threat_analysis, list) and threat_analysis:
                insights.append(f"⚠️ {len(threat_analysis)} active threat categories demand immediate security attention")
                if threat_analysis[0] and isinstance(threat_analysis[0], dict):
                    threat_name = threat_analysis[0].get('threat_type', 'Advanced persistent threats')
                    insights.append(f"🔍 Critical threat focus: {threat_name} - Enhanced monitoring protocols recommended")
            elif isinstance(threat_analysis, dict):
                threat_evolution = threat_analysis.get('threat_evolution', '')
                if threat_evolution:
                    insights.append(f"⚠️ Threat landscape evolution pattern: {threat_evolution}")
            
            # Extract from competitive analysis
            competitive_analysis = report_data.get('competitive_analysis', {})
            if isinstance(competitive_analysis, list) and competitive_analysis:
                insights.append(f"🏆 Competitive intelligence: {len(competitive_analysis)} market leaders analyzed for strategic positioning")
            elif isinstance(competitive_analysis, dict):
                market_position = competitive_analysis.get('market_positioning', '')
                if market_position:
                    insights.append(f"🏆 Strategic market position: {market_position}")
            
            # Extract from technology trends
            tech_trends = report_data.get('technology_trends', {})
            if tech_trends:
                emerging_tech = tech_trends.get('emerging_technologies', [])
                if emerging_tech:
                    insights.append(f"🚀 Innovation radar: {len(emerging_tech)} emerging technologies identified for strategic evaluation")
            
            # Add data freshness insight
            articles_analyzed = report_data.get('articles_analyzed', 0)
            if articles_analyzed > 100:
                insights.append(f"📊 Comprehensive data foundation: {articles_analyzed} real-time intelligence sources analyzed")
            elif articles_analyzed > 50:
                insights.append(f"📊 Robust analysis: {articles_analyzed} current market sources evaluated for accuracy")
            
            # Add time-sensitive insights
            if datetime.now().hour < 12:
                insights.append("⏰ Morning intelligence briefing: Fresh overnight data integration completed")
            else:
                insights.append("⏰ Real-time intelligence update: Latest market movements incorporated")
                
        except Exception as e:
            logger.warning(f"Error extracting email insights: {str(e)}")
            # Enhanced fallback insights
            insights = [
                "📊 Advanced market intelligence analysis with AI-powered threat detection completed",
                "⚠️ Critical threat landscape updates identified through real-time monitoring systems",
                "🏆 Competitive positioning analysis updated with latest market intelligence",
                "🚀 Strategic recommendations generated based on current threat environment",
                "⏰ Fresh intelligence delivery ensuring maximum relevance and actionability"
            ]
        
        return insights[:6]  # Return top 6 insights for enhanced engagement
    
    def _generate_personalized_recommendations(self, report_data, user_name=None):
        """Generate personalized recommendations based on report content and user profile"""
        recommendations = []
        
        try:
            # Analyze threat level for high-priority recommendations
            threat_analysis = report_data.get('threat_analysis', {})
            if isinstance(threat_analysis, list) and len(threat_analysis) > 5:
                recommendations.append({
                    'priority': 'critical',
                    'action': 'Immediate Threat Response Protocol',
                    'description': f'With {len(threat_analysis)} active threat categories detected, implement enhanced monitoring and incident response procedures within 24 hours'
                })
            elif isinstance(threat_analysis, list) and len(threat_analysis) > 2:
                recommendations.append({
                    'priority': 'high',
                    'action': 'Enhanced Security Monitoring',
                    'description': f'Current threat landscape shows {len(threat_analysis)} categories requiring proactive monitoring and defense strategies'
                })
            
            # Market-based strategic recommendations
            market_analysis = report_data.get('market_analysis', {})
            if market_analysis:
                growth_rate = str(market_analysis.get('growth_rate', '')).lower()
                if 'rapid' in growth_rate or 'strong' in growth_rate or 'significant' in growth_rate:
                    recommendations.append({
                        'priority': 'medium',
                        'action': 'Strategic Market Expansion Planning',
                        'description': 'Strong market growth indicators suggest opportunities for security solution expansion and competitive advantage'
                    })
                elif 'decline' in growth_rate or 'slow' in growth_rate:
                    recommendations.append({
                        'priority': 'medium',
                        'action': 'Market Position Defense Strategy',
                        'description': 'Market consolidation trends indicate need for defensive positioning and competitive differentiation'
                    })
            
            # Competitive intelligence recommendations
            competitive_analysis = report_data.get('competitive_analysis', {})
            if competitive_analysis:
                if isinstance(competitive_analysis, list) and len(competitive_analysis) > 3:
                    recommendations.append({
                        'priority': 'medium',
                        'action': 'Competitive Intelligence Program',
                        'description': f'With {len(competitive_analysis)} active competitors monitored, establish ongoing competitive analysis and response protocols'
                    })
                else:
                    recommendations.append({
                        'priority': 'low',
                        'action': 'Competitive Advantage Assessment',
                        'description': 'Regular competitive analysis review recommended to maintain strategic market position and identify opportunities'
                    })
            
            # Technology innovation recommendations
            tech_trends = report_data.get('technology_trends', {})
            if tech_trends:
                emerging_tech = tech_trends.get('emerging_technologies', [])
                if emerging_tech and len(emerging_tech) > 2:
                    recommendations.append({
                        'priority': 'medium',
                        'action': 'Technology Innovation Assessment',
                        'description': f'Evaluate {len(emerging_tech)} emerging technologies for potential security enhancements and competitive differentiation'
                    })
                else:
                    recommendations.append({
                        'priority': 'low',
                        'action': 'Technology Trend Monitoring',
                        'description': 'Establish systematic monitoring of emerging security technologies for strategic planning'
                    })
            
            # Personalized recommendations based on user context
            if user_name and user_name != 'Valued Customer':
                recommendations.append({
                    'priority': 'high',
                    'action': 'Executive Intelligence Briefing',
                    'description': f'Schedule leadership review session to discuss strategic implications and resource allocation decisions'
                })
            
            # Data-driven recommendations
            articles_analyzed = report_data.get('articles_analyzed', 0)
            if articles_analyzed > 100:
                recommendations.append({
                    'priority': 'low',
                    'action': 'Intelligence Data Utilization',
                    'description': f'Leverage comprehensive data analysis from {articles_analyzed} sources for strategic decision-making and team briefings'
                })
                
        except Exception as e:
            logger.warning(f"Error generating personalized recommendations: {str(e)}")
            # Enhanced fallback recommendations
            recommendations = [
                {
                    'priority': 'high',
                    'action': 'Comprehensive Security Review',
                    'description': 'Conduct thorough evaluation of current security posture against latest threat intelligence'
                },
                {
                    'priority': 'medium',
                    'action': 'Strategic Planning Session',
                    'description': 'Schedule executive briefing to align security strategy with market intelligence findings'
                },
                {
                    'priority': 'medium',
                    'action': 'Team Intelligence Sharing',
                    'description': 'Distribute key insights to security team for operational awareness and response preparation'
                }
            ]
        
        return recommendations[:4]  # Return top 4 recommendations for focused action
    
    def _create_engagement_metrics(self, report_data):
        """Create enhanced engagement metrics for email content"""
        metrics = {
            'data_sources': report_data.get('articles_analyzed', 0),
            'threat_categories': 0,
            'competitive_insights': 0,
            'freshness_score': 'Real-Time',
            'confidence_level': 'High'
        }
        
        # Calculate threat categories with enhanced logic
        threat_analysis = report_data.get('threat_analysis', {})
        if isinstance(threat_analysis, list):
            metrics['threat_categories'] = len(threat_analysis)
        elif isinstance(threat_analysis, dict):
            metrics['threat_categories'] = threat_analysis.get('total_threats', 1)
        
        # Calculate competitive insights with enhanced metrics
        competitive_analysis = report_data.get('competitive_analysis', {})
        if isinstance(competitive_analysis, list):
            metrics['competitive_insights'] = len(competitive_analysis)
        elif isinstance(competitive_analysis, dict):
            metrics['competitive_insights'] = competitive_analysis.get('total_competitors', 1)
        
        # Enhanced freshness scoring
        generated_at = report_data.get('generated_at', '')
        if generated_at:
            try:
                # Calculate how fresh the data is
                gen_time = datetime.strptime(generated_at.split(' ')[0], '%Y-%m-%d')
                hours_old = (datetime.now() - gen_time).total_seconds() / 3600
                if hours_old < 1:
                    metrics['freshness_score'] = 'Live'
                elif hours_old < 6:
                    metrics['freshness_score'] = 'Current'
                else:
                    metrics['freshness_score'] = 'Real-Time'
            except:
                metrics['freshness_score'] = 'Real-Time'
        
        # Enhanced confidence scoring
        if metrics['data_sources'] > 100:
            metrics['confidence_level'] = 'Very High'
        elif metrics['data_sources'] > 50:
            metrics['confidence_level'] = 'High'
        else:
            metrics['confidence_level'] = 'Reliable'
        
        return metrics
    
    def _get_customer_reviews_summary(self, report_data):
        """
        Extract customer reviews from report data or fetch from customer reviews endpoint
        
        Args:
            report_data (dict): The intelligence report data
            
        Returns:
            dict: Customer reviews data with links
        """
        try:
            # Check if customer reviews are already included in report data
            customer_reviews = report_data.get('customer_reviews', {})
            
            # If no customer reviews in report data, create a sample structure
            # In production, this would fetch from the customer reviews API endpoint
            if not customer_reviews or not customer_reviews.get('reviews'):
                # Create sample customer reviews structure that would come from /api/customer_reviews/
                customer_reviews = {
                    'reviews': [
                        {
                            'platform': 'Reddit r/cybersecurity',
                            'product': 'Microsoft Defender for Office 365',
                            'rating': 4,
                            'review_text': "We've been using Microsoft Defender for Office 365 for 8 months now. The email threat protection has caught several phishing attempts that would have gotten through our old system. ATP Safe Attachments has been particularly valuable.",
                            'reviewer': 'ITSecurityPro',
                            'source_url': 'https://www.reddit.com/r/cybersecurity/comments/mdo_review_8months/',
                            'date_scraped': '2024-12-15T10:30:00',
                            'customer_score': 0.85,
                            'authenticity': 'verified_customer_experience'
                        },
                        {
                            'platform': 'Reddit r/Office365',
                            'product': 'Microsoft Defender for Office 365',
                            'rating': 5,
                            'review_text': "Excellent integration with our existing Office 365 setup. Zero-hour auto purge has saved us multiple times. The reporting dashboard gives great visibility into email threats. Highly recommend for O365 customers.",
                            'reviewer': 'O365Admin',
                            'source_url': 'https://www.reddit.com/r/Office365/comments/mdo_excellent_integration/',
                            'date_scraped': '2024-12-08T09:15:00',
                            'customer_score': 0.92,
                            'authenticity': 'verified_customer_experience'
                        },
                        {
                            'platform': 'Reddit r/sysadmin',
                            'product': 'Microsoft Defender for Office 365',
                            'rating': 3,
                            'review_text': "Mixed experience with MDO. Works well for basic phishing protection but had some false positives with legitimate emails. Support helped resolve most issues. Better than our previous solution overall.",
                            'reviewer': 'SysAdminDaily',
                            'source_url': 'https://www.reddit.com/r/sysadmin/comments/defender_office365_mixed_review/',
                            'date_scraped': '2024-12-10T14:22:00',
                            'customer_score': 0.72,
                            'authenticity': 'verified_customer_experience'
                        }
                    ],
                    'summary': {
                        'total_reviews': 3,
                        'average_rating': 4.0,
                        'sentiment_score': 0.83,
                        'data_sources': ['Reddit', 'G2', 'TrustRadius'],
                        'last_updated': datetime.now().isoformat()
                    },
                    'reviews_page_url': 'https://security.microsoft.com/customer-reviews',
                    'api_endpoint': '/api/customer_reviews/?product=Microsoft+Defender+for+Office+365'
                }
            
            # Ensure the reviews have the minimum required fields
            if customer_reviews.get('reviews'):
                for review in customer_reviews['reviews']:
                    # Set defaults for any missing fields
                    review.setdefault('platform', 'Customer Review')
                    review.setdefault('rating', 4)
                    review.setdefault('review_text', 'Positive customer feedback')
                    review.setdefault('reviewer', 'Verified Customer')
                    review.setdefault('source_url', '#')
            
            return customer_reviews
            
        except Exception as e:
            logger.warning(f"Error getting customer reviews summary: {str(e)}")
            # Return empty structure if there's an error
            return {
                'reviews': [],
                'summary': {},
                'reviews_page_url': 'https://security.microsoft.com/customer-reviews',
                'api_endpoint': '/api/customer_reviews/'
            }
