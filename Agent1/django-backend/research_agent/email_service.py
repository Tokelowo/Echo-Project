"""
Email service for delivering research reports
"""
import os
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from .models import EmailDelivery, Report
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending research reports via email"""
    
    def __init__(self):
        # Email configuration from Django settings
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@microsoft.com')
        self.use_console_backend = settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend'
    
    def send_report_email(self, report: Report, recipient_email: str, recipient_name: str = None):
        """
        Send a research report via email using Django's email system
        """
        try:
            # Create email delivery record
            delivery = EmailDelivery.objects.create(
                report=report,
                recipient_email=recipient_email,
                recipient_name=recipient_name or "Research Subscriber",
                subject=f"MDO Research Report: {report.title}",
                status="queued"
            )
            
            # Create HTML and text content
            html_content = self._create_email_html(report, recipient_name, recipient_email)
            text_content = self._create_email_text(report, recipient_name)
            
            if self.use_console_backend:
                # Development mode - log to console
                logger.info(f"EMAIL DELIVERY (Console Mode):")
                logger.info(f"To: {recipient_email}")
                logger.info(f"Subject: {delivery.subject}")
                logger.info(f"Content Preview: {text_content[:200]}...")
                
                delivery.status = "sent"
                delivery.sent_at = timezone.now()
                delivery.save()
                
                return delivery
            
            # Production mode - send actual email using Django
            msg = EmailMultiAlternatives(
                subject=delivery.subject,
                body=text_content,
                from_email=self.from_email,
                to=[recipient_email]
            )
            msg.attach_alternative(html_content, "text/html")
            
            # Send the email
            msg.send()
            
            # Update delivery status
            delivery.status = "sent"
            delivery.sent_at = timezone.now()
            delivery.save()
            
            logger.info(f"Report email sent successfully to {recipient_email}")
            return delivery
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            if 'delivery' in locals():
                delivery.status = "failed"
                delivery.error_message = str(e)
                delivery.save()
            raise e

    def _create_email_html(self, report: Report, recipient_name: str = None, recipient_email: str = None):
        """Create HTML email content"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{report.title}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #0078d4 0%, #1a365d 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .logo {{ font-size: 24px; font-weight: bold; margin-bottom: 10px; }}
                .content {{ background: white; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .insights {{ background: #f8f9fa; padding: 20px; border-left: 4px solid #0078d4; margin: 20px 0; }}
                .footer {{ background: #f8f9fa; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; font-size: 14px; color: #666; }}
                .report-content {{ background: #ffffff; border: 1px solid #e1e5e9; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                .metadata {{ display: flex; justify-content: space-between; margin-bottom: 20px; }}
                .metadata div {{ background: #f1f3f4; padding: 10px; border-radius: 5px; }}
                ul {{ padding-left: 20px; }}
                li {{ margin-bottom: 8px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">Microsoft Defender for Office 365</div>
                <h1>{report.title}</h1>
                <p>AI-Generated Research Report | {report.created_at.strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="content">
                <p>Hello {recipient_name or 'there'},</p>
                <p>Your requested research report has been generated and is ready for review.</p>
                  <div class="metadata">
                    <div><strong>Agent:</strong> {getattr(report, 'agent', None) and report.agent.name or 'AI Research Agent'}</div>
                    <div><strong>Format:</strong> {getattr(report, 'get_format_display', lambda: 'JSON')()}</div>
                    <div><strong>Confidence:</strong> {getattr(report, 'confidence_score', None) or 'N/A'}</div>
                </div>
                  <div class="report-content">
                    <h3>Report Content</h3>
                    <pre style="white-space: pre-wrap; font-family: 'Segoe UI', sans-serif; background: #f8f9fa; padding: 20px; border-radius: 8px; font-size: 14px; line-height: 1.6;">{self._create_email_text(report, recipient_name)}</pre>
                </div>
                
                {self._format_insights_html(report)}
                  <div style="margin-top: 30px; padding: 20px; background: #e8f4fd; border-radius: 8px;">
                    <h4 style="margin-top: 0; color: #0078d4;">📊 Report Summary</h4>
                    <p><strong>Word Count:</strong> {getattr(report, 'word_count', 0)}</p>
                    <p><strong>Generated by:</strong> {getattr(report, 'agent', None) and report.agent.name or 'AI Research Agent'}</p>
                    <p><strong>Confidence Score:</strong> {getattr(report, 'confidence_score', None) or 'N/A'}</p>
                </div>
            </div>
            
            <div class="footer">
                <p><span class="logo">Microsoft Defender for Office 365</span> | Research Intelligence Platform</p>
                <p>This report was automatically generated by AI research agents.</p>
                <p style="font-size: 12px; margin-top: 15px;">
                    This email was sent to {recipient_email or 'your email address'}. If you no longer wish to receive these reports, please contact your administrator.
                </p>
            </div>
        </body>        </html>        """    
    def _create_email_text(self, report: Report, recipient_name: str = None):
        """Create professional executive email content for Microsoft PMs"""
        from .email_service_professional import create_professional_email_content
        return create_professional_email_content(report, recipient_name)
        email_content = f"""
========================================
MICROSOFT DEFENDER FOR OFFICE 365
EMAIL SECURITY MARKET INTELLIGENCE REPORT
========================================

REPORT: {report_data.get('title', report.title)}
Generated: {report.created_at.strftime('%B %d, %Y at %I:%M %p')}
Analysis Period: Real-time cybersecurity intelligence
Data Sources: Industry leading cybersecurity publications

========================================
📊 EXECUTIVE SUMMARY
========================================

{report_data.get('executive_summary', 'Comprehensive analysis of current cybersecurity landscape based on recent industry articles.')}

KEY METRICS:
• Articles Analyzed: {report_data.get('articles_analyzed', report_data.get('total_articles', 'Real-time data'))}
• Market Vendors Tracked: {len(report_data.get('market_presence', {}))}
• Technology Trends Identified: {len([k for k, v in report_data.get('technology_trends', {}).items() if v > 0])}
• Active Threats Detected: {len([k for k, v in report_data.get('threat_landscape', {}).items() if v > 0])}

========================================
📰 ARTICLE HEADLINES ANALYZED
========================================
"""

        # Add recent article headlines if available
        articles_list = report_data.get('articles', [])
        if articles_list:
            email_content += "\nRECENT CYBERSECURITY NEWS:\n"
            for i, article in enumerate(articles_list[:8], 1):
                title = article.get('title', 'No title')
                source = article.get('source', 'Unknown source')
                priority = article.get('priority', 'medium')
                priority_icon = "🔴" if priority == 'critical' else "🟡" if priority == 'high' else "🟢"
                email_content += f"\n{i}. {priority_icon} {title}\n   Source: {source} | Priority: {priority.upper()}\n"
        else:
            email_content += "\n• Real-time analysis of current cybersecurity news from leading sources"
            email_content += "\n• Sources include: BleepingComputer, SecurityWeek, The Hacker News, CyberNews"

        email_content += f"""

========================================
🔍 TECHNOLOGY TRENDS ANALYSIS
========================================

CURRENT MARKET BUZZ:"""
        # Add technology trends
        tech_trends = report_data.get('technology_trends', {})
        if tech_trends:
            sorted_trends = sorted(tech_trends.items(), key=lambda x: x[1], reverse=True)
            for i, (tech, mentions) in enumerate(sorted_trends[:8]):
                if mentions > 0:
                    priority = "🔥 CRITICAL FOCUS" if i == 0 else "📈 EMERGING PRIORITY" if i == 1 else "👀 MONITOR"
                    impact = 'AI/ML driving automation demands' if 'AI' in tech.upper() else 'Growing market adoption' if mentions > 2 else 'Emerging technology trend'
                    email_content += f"""
• {tech.upper()}: {mentions} mentions ({priority})
  Strategic Impact: {impact}
"""
        else:
            email_content += "\n• No specific technology trends detected in current analysis period"

        # Add competitive intelligence
        email_content += f"""

========================================
🏢 COMPETITIVE INTELLIGENCE
========================================

MARKET PRESENCE ANALYSIS:"""        
        market_presence = report_data.get('market_presence', {})
        if market_presence:
            sorted_vendors = sorted(market_presence.items(), key=lambda x: x[1].get('articles_count', 0), reverse=True)
            for vendor, data in sorted_vendors:
                articles = data.get('articles_count', 0)
                security_mentions = data.get('security_mentions', 0)
                market_score = data.get('market_score', 0)
                threat_mentions = data.get('threat_protection_mentions', 0)
                
                status = "🏆 LEADING" if articles > 1 else "📊 ACTIVE" if articles > 0 else "📉 QUIET"
                email_content += f"""
• {vendor.upper()}:
  - News Articles: {articles} 
  - Security Mentions: {security_mentions}
  - Threat Protection: {threat_mentions}
  - Market Score: {market_score}
  - Status: {status}
  - Strategic Context: {'High market visibility - monitor closely' if articles > 1 else 'Standard presence - opportunity for differentiation' if articles > 0 else 'Low activity - potential market gap'}
"""
        else:
            email_content += "\n• No competitive intelligence data available for current analysis period"

        # Add detailed threat analysis
        email_content += f"""

========================================
⚠️ THREAT LANDSCAPE & IMPLICATIONS
========================================

CURRENT THREAT ACTIVITY:"""
        
        threat_landscape = report_data.get('threat_landscape', {})
        if threat_landscape:
            active_threats = [(threat, count) for threat, count in threat_landscape.items() if count > 0]
            if active_threats:
                sorted_threats = sorted(active_threats, key=lambda x: x[1], reverse=True)
                for threat, incidents in sorted_threats:
                    severity = "🔴 CRITICAL" if incidents > 3 else "🟡 ELEVATED" if incidents > 1 else "🟢 NORMAL"
                    email_content += f"""
• {threat.upper()}: {incidents} incidents detected ({severity})
  Risk Level: {'Immediate attention required' if incidents > 3 else 'Monitor closely' if incidents > 1 else 'Standard monitoring'}
"""
            else:
                email_content += "\n• No immediate threats detected in current analysis period"
        else:
            email_content += "\n• No threat landscape data available for current analysis period"
        
        # Add strategic recommendations
        email_content += f"""

========================================
📈 STRATEGIC RECOMMENDATIONS FOR MDO
========================================

IMMEDIATE ACTIONS (Next 30 Days):
• Technology Focus: Emphasize {sorted_trends[0][0].upper() if 'sorted_trends' in locals() and sorted_trends else 'AI/ML'} capabilities in marketing campaigns
• Competitive Strategy: {"Monitor high-activity competitors closely" if any(d.get('articles_count', 0) > 2 for d in market_presence.values()) else "Opportunity for thought leadership in quiet market"}
• Threat Response: Priority focus on {sorted_threats[0][0].upper() if 'sorted_threats' in locals() and sorted_threats else 'MALWARE'} protection messaging

MARKET INTELLIGENCE:
• Market Activity Level: {"High competition period" if sum(d.get('articles_count', 0) for d in market_presence.values()) > 8 else "Moderate activity - opportunity window"}
• Technology Innovation: {"High buzz cycle - time for aggressive positioning" if sum(tech_trends.values()) > 10 else "Quiet innovation period - lead with thought leadership"}

========================================
🎯 KEY PERFORMANCE INDICATORS
========================================

MARKET POSITION METRICS:
• News Mentions Target: 2+ weekly mentions
• Security Coverage Ratio: 50%+ of mentions
• Technology Leadership: Lead in {sorted_trends[0][0].upper() if 'sorted_trends' in locals() and sorted_trends else 'AI/ML'} discussions

COMPETITIVE METRICS:
• Market Share Target: 40% within 12 months  
• Win Rate vs Key Competitors: Track performance against Proofpoint/Mimecast
• Customer Retention: Monitor and expand existing accounts

========================================
📊 REPORT METADATA
========================================

Report ID: {report.id}
Agent Type: {report_data.get('agent_type', 'comprehensive_research')}
Generation Time: {report.created_at.isoformat()}
Data Freshness: Real-time analysis
Classification: Microsoft Internal Use Only

========================================

Best regards,
MDO Research Intelligence Platform
Microsoft Defender for Office 365

This report contains AI-generated insights based on real-time cybersecurity intelligence.
For questions about this report, contact your MDO research team.
        """
        
        return email_content

    def _format_insights_html(self, report: Report):
        """Format insights for HTML email"""
        if report.key_insights:
            insights_html = '<ul>'
            for insight in report.key_insights[:5]:  # Limit to 5 insights
                insights_html += f'<li>{insight}</li>'
            insights_html += '</ul>'
            
            return f"""
                <div class="insights">
                    <h4 style="margin-top: 0; color: #0078d4;">🔍 Key Insights</h4>
                    {insights_html}
                </div>
            """
        return ''

    def _format_insights_text(self, report: Report):
        """Format insights for plain text email"""
        if report.key_insights:
            insights = '\\n'.join([f"• {insight}" for insight in report.key_insights[:5]])
            return insights
        return 'No specific insights extracted.'

# Convenience function for easy import
def send_report_email(report: Report, recipient_email: str, recipient_name: str = None):
    """Send a report via email"""
    service = EmailService()
    return service.send_report_email(report, recipient_email, recipient_name)
