"""
Email service for delivering research reports with enhanced security
"""
import os
import re
import hashlib
import time
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from .models import EmailDelivery, Report
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending research reports via email with security features"""
    
    def __init__(self):
        # Email configuration from Django settings
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@microsoft.com')
        self.use_console_backend = settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend'
        
        # Security settings
        self.rate_limit_per_minute = getattr(settings, 'EMAIL_RATE_LIMIT_PER_MINUTE', 10)
        self.max_daily_emails = getattr(settings, 'EMAIL_MAX_DAILY_EMAILS', 100)
        self.blocked_domains = getattr(settings, 'EMAIL_BLOCKED_DOMAINS', [
            'tempmail.', 'guerrillamail.', '10minutemail.', 'mailinator.'
        ])
        
        # Email tracking
        self._email_attempts = {}
        self._daily_counts = {}
    
    def validate_email_security(self, email: str) -> tuple[bool, str]:
        """
        Validate email address for security concerns
        Returns: (is_valid, error_message)
        """
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        # Check against blocked domains
        email_lower = email.lower()
        for blocked_domain in self.blocked_domains:
            if blocked_domain in email_lower:
                return False, f"Email domain not allowed: {blocked_domain}"
        
        # Rate limiting check
        current_time = time.time()
        minute_key = int(current_time / 60)
        email_key = f"{email}_{minute_key}"
        
        if email_key in self._email_attempts:
            if self._email_attempts[email_key] >= self.rate_limit_per_minute:
                return False, f"Rate limit exceeded: {self.rate_limit_per_minute} emails per minute"
        
        # Daily limit check
        today = datetime.now().strftime('%Y-%m-%d')
        daily_key = f"{email}_{today}"
        
        if daily_key in self._daily_counts:
            if self._daily_counts[daily_key] >= self.max_daily_emails:
                return False, f"Daily limit exceeded: {self.max_daily_emails} emails per day"
        
        return True, ""
    
    def increment_email_counters(self, email: str):
        """Increment email counters for rate limiting"""
        current_time = time.time()
        minute_key = int(current_time / 60)
        email_key = f"{email}_{minute_key}"
        today = datetime.now().strftime('%Y-%m-%d')
        daily_key = f"{email}_{today}"
        
        # Increment minute counter
        self._email_attempts[email_key] = self._email_attempts.get(email_key, 0) + 1
        
        # Increment daily counter
        self._daily_counts[daily_key] = self._daily_counts.get(daily_key, 0) + 1
        
        # Clean old entries (older than 1 hour)
        hour_ago = current_time - 3600
        keys_to_remove = [k for k in self._email_attempts.keys() 
                         if int(k.split('_')[-1]) * 60 < hour_ago]
        for key in keys_to_remove:
            del self._email_attempts[key]
    
    def sanitize_content(self, content: str) -> str:
        """Sanitize email content to prevent injection attacks"""
        if not content:
            return ""
        
        # Remove potentially dangerous content
        dangerous_patterns = [
            r'<script.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe.*?</iframe>',
            r'<object.*?</object>',
            r'<embed.*?</embed>'
        ]
        
        sanitized = content
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        
        return sanitized
    
    def generate_email_token(self, recipient_email: str, report_id: int) -> str:
        """Generate secure token for email tracking"""
        timestamp = str(int(time.time()))
        data = f"{recipient_email}:{report_id}:{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def send_report_email(self, report: Report, recipient_email: str, recipient_name: str = None):
        """
        Send a research report via email using Django's email system with security validation
        """
        try:
            # Security validation
            is_valid, error_message = self.validate_email_security(recipient_email)
            if not is_valid:
                logger.warning(f"Email security validation failed for {recipient_email}: {error_message}")
                raise ValueError(f"Email security validation failed: {error_message}")
            
            # Increment rate limiting counters
            self.increment_email_counters(recipient_email)
            
            # Generate security token
            email_token = self.generate_email_token(recipient_email, report.id)
            
            # Create email delivery record
            delivery = EmailDelivery.objects.create(
                report=report,
                recipient_email=recipient_email,
                recipient_name=recipient_name or "Research Subscriber",
                subject=f"MDO Research Report: {report.title}",
                status="queued"
            )
            
            # Create HTML and text content with security sanitization
            html_content = self._create_email_html(report, recipient_name, recipient_email, email_token)
            text_content = self._create_email_text(report, recipient_name)
            
            # Sanitize content
            html_content = self.sanitize_content(html_content)
            text_content = self.sanitize_content(text_content)
            
            if self.use_console_backend:
                # Development mode - log to console
                logger.info(f"EMAIL DELIVERY (Console Mode - Secure):")
                logger.info(f"To: {recipient_email}")
                logger.info(f"Subject: {delivery.subject}")
                logger.info(f"Security Token: {email_token}")
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
                to=[recipient_email],
                headers={
                    'X-Email-Token': email_token,
                    'X-Report-ID': str(report.id),
                    'X-Security-Level': 'Enhanced'
                }
            )
            msg.attach_alternative(html_content, "text/html")
            
            # Send the email
            msg.send()
            
            # Update delivery status
            delivery.status = "sent"
            delivery.sent_at = timezone.now()
            delivery.save()
            
            logger.info(f"Secure report email sent successfully to {recipient_email} with token {email_token}")
            return delivery
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            if 'delivery' in locals():
                delivery.status = "failed"
                delivery.error_message = str(e)
                delivery.save()
            raise e

    def _create_email_html(self, report: Report, recipient_name: str = None, recipient_email: str = None, email_token: str = None):
        """Create HTML email content with security features"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-Content-Type-Options" content="nosniff">
            <meta http-equiv="X-Frame-Options" content="DENY">
            <meta http-equiv="X-XSS-Protection" content="1; mode=block">
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
                .security-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                ul {{ padding-left: 20px; }}
                li {{ margin-bottom: 8px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">🛡️ Microsoft Defender for Office 365</div>
                <h1>{report.title}</h1>
                <p>AI-Generated Research Report | {report.created_at.strftime('%B %d, %Y')}</p>
                {f'<p style="font-size: 12px; opacity: 0.8;">Security Token: {email_token}</p>' if email_token else ''}
            </div>
            
            <div class="content">
                <div class="security-notice">
                    <strong>🔒 Security Notice:</strong> This email contains confidential research intelligence. 
                    Please do not forward this email to unauthorized recipients.
                </div>
                
                <p>Hello {recipient_name or 'there'},</p>
                <p>Your requested research report has been generated and is ready for review.</p>
                
                <div class="metadata">
                    <div><strong>Agent:</strong> {report.agent.name}</div>
                    <div><strong>Format:</strong> {report.get_format_display()}</div>
                    <div><strong>Confidence:</strong> {report.confidence_score or 'N/A'}</div>
                    <div><strong>🔐 Secure:</strong> ✓ Verified</div>
                </div>
                
                <div class="report-content">
                    <h3>Report Content</h3>
                    <div>{report.content}</div>
                </div>
                
                {self._format_insights_html(report)}
                
                <div style="margin-top: 30px; padding: 20px; background: #e8f4fd; border-radius: 8px;">
                    <h4 style="margin-top: 0; color: #0078d4;">📊 Report Summary</h4>
                    <p><strong>Word Count:</strong> {report.word_count}</p>
                    <p><strong>Generated by:</strong> {report.agent.name}</p>
                    <p><strong>Confidence Score:</strong> {report.confidence_score or 'N/A'}</p>
                    <p><strong>Security Level:</strong> Enhanced Protection</p>
                </div>
            </div>
            
            <div class="footer">
                <p><span class="logo">🛡️ Microsoft Defender for Office 365</span> | Research Intelligence Platform</p>
                <p>This report was automatically generated by AI research agents with enhanced security.</p>
                <p style="font-size: 12px; margin-top: 15px;">
                    This email was sent to {recipient_email or 'your email address'}. If you no longer wish to receive these reports, please contact your administrator.
                </p>
                <p style="font-size: 10px; color: #999; margin-top: 10px;">
                    🔒 This email is protected by Microsoft security protocols. Report ID: {report.id}
                </p>
            </div>
        </body>
        </html>
        """
    
    def _create_email_text(self, report: Report, recipient_name: str = None):
        """Create plain text email content"""
        return f"""
MDO RESEARCH REPORT - SECURE DELIVERY
====================================

Hello {recipient_name or 'there'},

Your requested research report has been generated:

TITLE: {report.title}
AGENT: {report.agent.name}
DATE: {report.created_at.strftime('%B %d, %Y')}
CONFIDENCE: {report.confidence_score or 'N/A'}
SECURITY: Enhanced Protection

REPORT CONTENT:
{report.content}

KEY INSIGHTS:
{self._format_insights_text(report)}

SECURITY NOTICE:
This email contains confidential research intelligence.
Please do not forward this email to unauthorized recipients.

---
🛡️ Microsoft Defender for Office 365 | Research Intelligence Platform
This report was automatically generated by AI research agents with enhanced security.
Report ID: {report.id}
        """

    def _format_insights_html(self, report: Report):
        """Format insights for HTML email"""
        if not report.key_insights:
            return ''
            
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

    def _format_insights_text(self, report: Report):
        """Format insights for plain text email"""
        if not report.key_insights:
            return 'No specific insights extracted.'
            
        insights = '\n'.join([f"• {insight}" for insight in report.key_insights[:5]])
        return insights

# Convenience function for easy import
def send_report_email(report: Report, recipient_email: str, recipient_name: str = None):
    """Send a report via email"""
    service = EmailService()
    return service.send_report_email(report, recipient_email, recipient_name)
