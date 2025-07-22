"""
Test Enhanced Email Content - Generate a sample email to preview enhancements
"""
import sys
import os

# Add the django project to Python path
sys.path.append('c:\\Users\\t-tokelowo\\OneDrive - Microsoft\\Agent 1\\django-backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from research_agent.enhanced_email_formatter import EnhancedEmailFormatter
from datetime import datetime

def test_enhanced_email():
    """Test the enhanced email formatter with sample data"""
    
    # Create sample report data
    sample_report_data = {
        'title': 'Weekly Email Security Intelligence Report',
        'executive_summary': 'This week\'s analysis reveals significant evolution in email-based threats, with phishing attacks increasing by 23% and new ransomware variants targeting Office 365 environments. Market consolidation continues as organizations prioritize integrated security solutions.',
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M UTC'),
        'articles_analyzed': 147,
        'market_analysis': {
            'growth_rate': 'Strong 18% YoY increase in email security investments',
            'growth_drivers': 'Remote work expansion and sophisticated threat evolution'
        },
        'threat_analysis': [
            {'threat_type': 'Advanced Phishing Campaigns', 'severity': 'high'},
            {'threat_type': 'Business Email Compromise', 'severity': 'critical'},
            {'threat_type': 'Ransomware Delivery via Email', 'severity': 'high'},
            {'threat_type': 'Account Takeover Attacks', 'severity': 'medium'},
            {'threat_type': 'Supply Chain Email Attacks', 'severity': 'high'}
        ],
        'competitive_analysis': [
            {'company': 'Proofpoint', 'market_share': '22%'},
            {'company': 'Mimecast', 'market_share': '18%'},
            {'company': 'Barracuda', 'market_share': '15%'}
        ],
        'technology_trends': {
            'emerging_technologies': ['AI-powered threat detection', 'Zero-trust email architecture', 'Behavioral analytics']
        },
        # Subscription-specific data
        'is_subscription_email': True,
        'subscription_frequency': 'weekly',
        'subscription_agent': 'intelligence_agent',
        'unsubscribe_url': 'https://localhost:3001/unsubscribe?token=sample123&email=test@example.com',
        'manage_subscription_url': 'https://localhost:3001/subscriptions?email=test@example.com'
    }
    
    # Create enhanced formatter
    formatter = EnhancedEmailFormatter()
    
    # Generate enhanced email content
    email_content = formatter.create_enhanced_email_summary(
        sample_report_data, 
        'John Smith',  # User name for personalization
        'Microsoft_Defender_Intelligence_Report_20250102_1430.docx'
    )
    
    # Save HTML content for preview
    html_file_path = 'c:\\Users\\t-tokelowo\\OneDrive - Microsoft\\Agent 1\\enhanced_email_preview.html'
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(email_content['html_body'])
    
    # Save plain text content for preview
    text_file_path = 'c:\\Users\\t-tokelowo\\OneDrive - Microsoft\\Agent 1\\enhanced_email_preview.txt'
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(email_content['plain_text_body'])
    
    print("✅ Enhanced Email Content Generated Successfully!")
    print(f"📧 Subject: {email_content['subject']}")
    print(f"📊 Engagement Score: {email_content.get('engagement_score', 'N/A')}")
    print(f"🎯 Personalization Level: {email_content.get('personalization_level', 'N/A')}")
    print(f"📄 HTML Preview: {html_file_path}")
    print(f"📝 Text Preview: {text_file_path}")
    print("\n" + "="*60)
    print("📋 EMAIL PREVIEW - First 500 characters:")
    print("="*60)
    print(email_content['plain_text_body'][:500] + "...")
    
    return email_content

if __name__ == "__main__":
    test_enhanced_email()
