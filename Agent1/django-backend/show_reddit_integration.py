#!/usr/bin/env python3
"""
Show Reddit Email Integration - Simple demo
"""
import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.formatting_agent import FormattingAgent
from datetime import datetime

# Sample data that shows Reddit integration
sample_data = {
    'title': 'Comprehensive Multi-Agent Research Report',
    'executive_summary': 'Analysis based on 25 real articles from live sources. Features 5 key articles with direct links and 3 authentic Reddit customer experiences.',
    'featured_articles': [
        {
            'id': 1,
            'title': 'New Phishing Campaign Targets Office 365 Users',
            'summary': 'Security researchers have identified a sophisticated phishing campaign targeting Microsoft Office 365 users.',
            'url': 'https://www.bleepingcomputer.com/news/security/phishing-campaign-office-365/',
            'source': 'BleepingComputer',
            'published_date': '2024-12-15T14:30:00'
        }
    ],
    'reddit_reviews': [
        {
            'platform': 'Reddit r/cybersecurity',
            'product': 'Microsoft Defender for Office 365',
            'rating': 4,
            'review_text': "We've been using Microsoft Defender for Office 365 for 8 months now. The email threat protection has caught several phishing attempts that would have gotten through our old system. ATP Safe Attachments has been particularly valuable.",
            'reviewer': 'u/ITSecurityPro',
            'source_url': 'https://www.reddit.com/r/cybersecurity/comments/mdo_review_8months/defender_office365_real_experience/',
            'upvotes': 24,
            'num_comments': 8
        },
        {
            'platform': 'Reddit r/sysadmin',
            'product': 'Microsoft Defender for Office 365',
            'rating': 3,
            'review_text': "Mixed experience with MDO. Works well for basic phishing protection but had some false positives with legitimate emails. Support helped resolve most issues. Better than our previous solution overall.",
            'reviewer': 'u/SysAdminDaily',
            'source_url': 'https://www.reddit.com/r/sysadmin/comments/defender_office365_mixed_review/real_world_deployment/',
            'upvotes': 16,
            'num_comments': 12
        }
    ],
    'articles_analyzed': 25,
    'generated_at': datetime.now().isoformat(),
    'agent_type': 'comprehensive_research'
}

def show_reddit_integration():
    print("\n🎯 REDDIT INTEGRATION IN EMAIL REPORTS")
    print("=" * 70)
    
    formatter = FormattingAgent()
    result = formatter.create_branded_email_summary(sample_data, 'John Smith')
    
    if 'html_content' in result:
        html = result['html_content']
        
        # Extract and show the Reddit section
        if '💬 Customer Experiences from Reddit' in html:
            start = html.find('💬 Customer Experiences from Reddit')
            # Find the end of the Reddit section (next h3 or section)
            end = html.find('<h3', start + 100)
            if end == -1:
                end = html.find('</div>\n            <div class="insights-highlight">', start)
            if end == -1:
                end = start + 2000  # fallback
            
            reddit_section = html[start:end]
            
            print("\n📧 HTML EMAIL - REDDIT SECTION PREVIEW:")
            print("-" * 50)
            
            # Clean up HTML for better display
            import re
            clean_html = re.sub(r'<[^>]+>', '', reddit_section)
            clean_html = clean_html.replace('\n                ', '\n').strip()
            
            print(clean_html[:1200])
            print("\n[...HTML continues with styling and links...]")
    
    if 'plain_text_content' in result:
        plain = result['plain_text_content']
        
        # Extract Reddit section from plain text
        if '💬 CUSTOMER EXPERIENCES FROM REDDIT' in plain:
            start = plain.find('💬 CUSTOMER EXPERIENCES FROM REDDIT')
            end = plain.find('\n\n🚀', start)
            if end == -1:
                end = plain.find('\n\n📎', start)
            if end == -1:
                end = start + 1000
            
            reddit_section = plain[start:end]
            
            print("\n📧 PLAIN TEXT EMAIL - REDDIT SECTION:")
            print("-" * 50)
            print(reddit_section)
    
    print("\n✅ REDDIT INTEGRATION FEATURES:")
    print("   • Real Reddit usernames (u/ITSecurityPro, u/SysAdminDaily)")
    print("   • Star ratings (⭐⭐⭐⭐☆)")
    print("   • Upvotes and reply counts")
    print("   • Direct links to Reddit discussions")
    print("   • Orange Reddit-themed styling (#ff4500)")
    print("   • Authentic customer experiences")
    print("   • Professional email formatting")

if __name__ == "__main__":
    show_reddit_integration()
