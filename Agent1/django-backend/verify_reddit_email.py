#!/usr/bin/env python3
"""
Verify Reddit reviews are included in email reports
"""
import os
import sys
import django
import json
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from research_agent.enhanced_email_service import EnhancedEmailService
from research_agent.formatting_agent import FormattingAgent
from research_agent.views import news_service

def test_reddit_email_integration():
    print("🔍 TESTING REDDIT EMAIL INTEGRATION")
    print("=" * 50)
    
    # Create test data with Reddit reviews
    reddit_reviews = [
        {
            'platform': 'Reddit r/cybersecurity',
            'product': 'Microsoft Defender for Office 365',
            'rating': 4,
            'review_text': "We've been using Microsoft Defender for Office 365 for 8 months now. The email threat protection has caught several phishing attempts that would have gotten through our old system. ATP Safe Attachments has been particularly valuable.",
            'reviewer': 'u/ITSecurityPro',
            'source_url': 'https://www.reddit.com/r/cybersecurity/comments/mdo_review_8months/defender_office365_real_experience/',
            'date_scraped': '2024-12-15T10:30:00',
            'upvotes': 24,
            'num_comments': 8,
            'customer_score': 0.85
        },
        {
            'platform': 'Reddit r/sysadmin', 
            'product': 'Microsoft Defender for Office 365',
            'rating': 3,
            'review_text': "Mixed experience with MDO. Works well for basic phishing protection but had some false positives with legitimate emails. Support helped resolve most issues. Better than our previous solution overall.",
            'reviewer': 'u/SysAdminDaily',
            'source_url': 'https://www.reddit.com/r/sysadmin/comments/defender_office365_mixed_review/real_world_deployment/',  
            'date_scraped': '2024-12-10T14:22:00',
            'upvotes': 16,
            'num_comments': 12,
            'customer_score': 0.72
        }
    ]
    
    # Get some real articles
    try:
        articles = news_service.fetch_cybersecurity_news(max_articles=5)
        print(f"✅ Fetched {len(articles)} real articles")
    except Exception as e:
        print(f"⚠️  Using sample articles due to: {str(e)}")
        articles = [
            {
                'title': 'Microsoft Defender Blocks New Phishing Campaign',
                'summary': 'Security researchers identified a new phishing campaign targeting Office 365 users',
                'url': 'https://example.com/news1',
                'source': 'Security News'
            }
        ]
    
    # Create comprehensive report data
    report_data = {
        'title': 'REDDIT INTEGRATION TEST - Comprehensive Multi-Agent Research Report',
        'executive_summary': f'TEST: Comprehensive analysis with {len(reddit_reviews)} authentic Reddit customer experiences and {len(articles)} real articles. This email should contain clickable Reddit links and a DOCX attachment.',
        'articles_analyzed': len(articles),
        'featured_articles': articles[:3],
        'reddit_reviews': reddit_reviews,  # This is the key data
        'agent_type': 'comprehensive_research',
        'data_sources': ['TechCrunch', 'BleepingComputer', 'The Hacker News', 'SecurityWeek', 'Reddit'], 
        'generated_at': datetime.now().isoformat(),
        'data_validation': {
            'reddit_reviews_included': len(reddit_reviews) > 0,
            'live_urls_verified': True,
            'test_mode': True
        }
    }
    
    print(f"📊 Report includes {len(reddit_reviews)} Reddit reviews:")
    for i, review in enumerate(reddit_reviews, 1):
        print(f"  {i}. {review['platform']} - Rating: {review['rating']}/5")
        print(f"     Link: {review['source_url']}")
        print(f"     Upvotes: {review['upvotes']}")
    
    # Test email formatting
    print("\n🔧 Testing email generation...")
    email_service = EnhancedEmailService()
    
    # Send test email
    result = email_service.send_professional_report_email(
        report_data,
        't-tokelowo@microsoft.com',
        'Temiloluwa Okelowo (Reddit Test)'
    )
    
    print(f"\n📧 EMAIL RESULT:")
    print(json.dumps(result, indent=2))
    
    # Also generate just the email content to show structure
    print("\n📝 EMAIL CONTENT PREVIEW:")
    formatting_agent = FormattingAgent()
    email_content = formatting_agent.create_branded_email_summary(
        report_data, 
        'Temiloluwa Okelowo (Reddit Test)',
        'test_reddit_report.docx'
    )
    
    print(f"Subject: {email_content['subject']}")
    print(f"HTML body length: {len(email_content['html_body'])} characters")
    print(f"Plain text body length: {len(email_content['plain_text_body'])} characters")
    
    # Check if Reddit content is in HTML
    if 'reddit' in email_content['html_body'].lower():
        print("✅ Reddit content found in HTML email")
    else:
        print("❌ Reddit content NOT found in HTML email")
        
    # Show Reddit section from HTML
    html_body = email_content['html_body']
    if 'reddit' in html_body.lower():
        start_idx = html_body.lower().find('reddit') - 100
        end_idx = html_body.lower().find('reddit') + 500
        reddit_section = html_body[max(0, start_idx):min(len(html_body), end_idx)]
        print(f"\n📱 REDDIT SECTION PREVIEW:")
        print(reddit_section[:500] + "..." if len(reddit_section) > 500 else reddit_section)
    
    print(f"\n🎯 WHAT YOU SHOULD RECEIVE:")
    print(f"1. Email with subject: {email_content['subject']}")
    print(f"2. DOCX attachment: {result.get('docx_filename', 'Unknown')}")
    print(f"3. Reddit reviews section with clickable links")
    print(f"4. Featured articles with real URLs")
    print(f"5. Professional Microsoft branding")
    
    return result

if __name__ == "__main__":
    test_reddit_email_integration()
