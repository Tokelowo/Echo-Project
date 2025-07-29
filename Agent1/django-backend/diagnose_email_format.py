#!/usr/bin/env python3
"""
DIAGNOSE EMAIL DISCREPANCY - Find why test vs production emails differ
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

def diagnose_email_issue():
    print("🔍 DIAGNOSING EMAIL FORMAT DISCREPANCY")
    print("=" * 60)
    
    # Create the EXACT same Reddit reviews data as the working test
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
    
    # Create sample articles
    featured_articles = [
        {
            'id': 1,
            'title': 'Hackers Deploy Stealth Backdoor in WordPress Mu-Plugins to Maintain Admin Access',
            'summary': 'Cybersecurity researchers have uncovered a new stealthy backdoor concealed within the "mu-plugins" directory in WordPress...',
            'url': 'https://thehackernews.com/wordpress-backdoor',
            'source': 'The Hacker News'
        },
        {
            'id': 2, 
            'title': 'US nuclear weapons agency hacked in Microsoft SharePoint attacks',
            'summary': 'Unknown threat actors have breached the National Nuclear Security Administration\'s network in attacks exploiting a recent...',
            'url': 'https://www.bleepingcomputer.com/nuclear-hack',
            'source': 'BleepingComputer'
        }
    ]
    
    # Create report data EXACTLY like the working test
    report_data = {
        'title': 'REDDIT INTEGRATION TEST - Comprehensive Multi-Agent Research Report',
        'executive_summary': f'TEST: Comprehensive analysis with {len(reddit_reviews)} authentic Reddit customer experiences and {len(featured_articles)} real articles. This email should contain clickable Reddit links and a DOCX attachment.',
        'featured_articles': featured_articles,
        'reddit_reviews': reddit_reviews,
        'articles_analyzed': len(featured_articles),
        'agent_type': 'comprehensive_research',
        'generated_at': datetime.now().isoformat(),
        'data_validation': {
            'reddit_reviews_included': len(reddit_reviews) > 0,
            'test_mode': True
        }
    }
    
    print(f"📊 Test data prepared:")
    print(f"   Reddit reviews: {len(reddit_reviews)}")
    print(f"   Featured articles: {len(featured_articles)}")
    
    # Test the formatting agent directly
    print("\n🔧 Testing FormattingAgent directly...")
    formatting_agent = FormattingAgent()
    
    try:
        email_content = formatting_agent.create_branded_email_summary(
            report_data,
            'Temiloluwa Okelowo (Diagnostic Test)',
            'test_report.docx'
        )
        
        html_body = email_content.get('html_body', '')
        
        print(f"✅ Email generated successfully")
        print(f"   Subject: {email_content.get('subject', 'N/A')}")
        print(f"   HTML body length: {len(html_body)} characters")
        
        # Check for Reddit content
        if 'reddit' in html_body.lower():
            print("✅ Reddit content found in HTML")
            
            # Extract Reddit section
            if '💬 Customer Experiences from Reddit' in html_body:
                reddit_start = html_body.find('💬 Customer Experiences from Reddit')
                reddit_section = html_body[reddit_start:reddit_start + 2000]
                
                print("\n📱 REDDIT SECTION FROM FORMATTING AGENT:")
                print("-" * 50)
                print(reddit_section)
                print("-" * 50)
                
                # Check for clickable links
                if 'https://www.reddit.com/r/' in reddit_section:
                    print("✅ Reddit URLs found in section")
                else:
                    print("❌ Reddit URLs NOT found in section")
                    
                # Check for star ratings
                if '⭐' in reddit_section:
                    print("✅ Star ratings found")
                else:
                    print("❌ Star ratings NOT found")
                    
        else:
            print("❌ Reddit content NOT found in HTML")
    
    except Exception as e:
        print(f"❌ Error with FormattingAgent: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Now test the EnhancedEmailService (what production uses)
    print("\n🔧 Testing EnhancedEmailService (Production Path)...")
    
    try:
        email_service = EnhancedEmailService()
        
        # This is what gets called in production
        result = email_service.send_professional_report_email(
            report_data,
            't-tokelowo@microsoft.com',
            'Temiloluwa Okelowo (Production Test)'
        )
        
        print(f"📧 EnhancedEmailService result:")
        print(json.dumps(result, indent=2))
        
        if result.get('status') == 'success':
            print("✅ Production email service working")
        else:
            print("❌ Production email service failed")
            
    except Exception as e:
        print(f"❌ Error with EnhancedEmailService: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print(f"\n🎯 SUMMARY:")
    print(f"   The test email that worked had Reddit reviews with clickable links")
    print(f"   If production emails don't match, the issue might be:")
    print(f"   1. Different data structure being passed")
    print(f"   2. Email client not rendering HTML properly")
    print(f"   3. DOCX attachment being blocked")
    print(f"   4. Email going to spam folder")

if __name__ == "__main__":
    diagnose_email_issue()
