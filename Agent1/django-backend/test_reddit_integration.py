#!/usr/bin/env python
"""
Test Reddit integration in email reports
"""
import os
import sys
import django
from datetime import datetime
import json

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.views import full_agent_pipeline
from research_agent.formatting_agent import FormattingAgent
from research_agent.cybersecurity_news_service_new import CybersecurityNewsService
from django.test import RequestFactory
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
import io


def test_reddit_reviews_integration():
    """Test that Reddit reviews are being included in email reports"""
    print("🧪 Testing Reddit Reviews Integration...")
    
    # Create a request factory
    factory = RequestFactory()
    
    # Create test request data
    test_data = {
        'input': 'Generate comprehensive research report with Reddit reviews',
        'agent_type': 'comprehensive_research',
        'user_email': 'test@microsoft.com',
        'user_name': 'Test User',
        'focus_areas': ['cybersecurity', 'reddit'],
        'delivery': {'email': True}
    }
    
    # Create mock request
    request = factory.post('/api/full-agent-pipeline', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    # Parse request as DRF request
    stream = io.BytesIO(json.dumps(test_data).encode())
    request.data = JSONParser().parse(stream)
    
    try:
        print("📊 Generating comprehensive research report...")
        
        # Call the view directly
        response = full_agent_pipeline(request)
        
        if hasattr(response, 'data'):
            report_data = response.data
            print(f"✅ Report generated successfully!")
            print(f"📈 Articles analyzed: {report_data.get('articles_analyzed', 0)}")
            
            # Check if Reddit reviews are included
            reddit_reviews = report_data.get('reddit_reviews', [])
            print(f"💬 Reddit reviews found: {len(reddit_reviews)}")
            
            if reddit_reviews:
                print("\n🎯 Reddit Reviews Sample:")
                for i, review in enumerate(reddit_reviews[:2], 1):
                    platform = review.get('platform', 'Unknown')
                    reviewer = review.get('reviewer', 'Anonymous')
                    rating = review.get('rating', 0)
                    text_preview = review.get('review_text', '')[:100] + "..."
                    url = review.get('source_url', '')
                    
                    print(f"  {i}. {reviewer} on {platform} - {rating}/5 stars")
                    print(f"     Preview: {text_preview}")
                    print(f"     URL: {url}")
                    print()
            
            # Test email formatting with Reddit reviews
            print("📧 Testing email formatting with Reddit reviews...")
            formatter = FormattingAgent()
            
            email_content = formatter.create_branded_email_summary(
                report_data, 
                user_name="Test User",
                docx_filename="test_report.docx"
            )
            
            html_body = email_content.get('html_body', '')
            plain_text = email_content.get('plain_text_body', '')
            
            # Check if Reddit section exists in email
            has_reddit_html = 'Customer Experiences from Reddit' in html_body
            has_reddit_plain = 'CUSTOMER EXPERIENCES FROM REDDIT' in plain_text
            
            print(f"✅ Reddit section in HTML email: {has_reddit_html}")
            print(f"✅ Reddit section in plain text email: {has_reddit_plain}")
            
            if has_reddit_html:
                print("🎉 Reddit reviews successfully integrated into email reports!")
                
                # Count Reddit review entries in HTML
                reddit_count_html = html_body.count('View Discussion →')
                print(f"📊 Reddit reviews in HTML email: {reddit_count_html}")
                
                # Save sample email for inspection
                with open('sample_email_with_reddit.html', 'w', encoding='utf-8') as f:
                    f.write(html_body)
                print("💾 Sample email saved as 'sample_email_with_reddit.html'")
            else:
                print("⚠️ Reddit reviews not found in email formatting")
            
            return True
        else:
            print(f"❌ Error in response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Reddit integration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_reddit_service_directly():
    """Test Reddit service directly"""
    print("\n🔍 Testing Reddit service directly...")
    
    try:
        news_service = CybersecurityNewsService()
        
        # Test Reddit reviews fetch
        reddit_reviews = news_service.real_reviews_service.fetch_reddit_discussions(
            'Microsoft Defender for Office 365', 
            max_reviews=3
        )
        
        print(f"📊 Direct Reddit service test: {len(reddit_reviews)} reviews found")
        
        if reddit_reviews:
            for i, review in enumerate(reddit_reviews, 1):
                print(f"  {i}. {review.get('reviewer', 'Unknown')} - {review.get('rating', 0)}/5")
                print(f"     Platform: {review.get('platform', 'Unknown')}")
                print(f"     URL: {review.get('source_url', 'N/A')}")
        
        return len(reddit_reviews) > 0
        
    except Exception as e:
        print(f"❌ Direct Reddit service error: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Reddit Reviews Integration Test")
    print("="*60)
    
    # Test Reddit service directly first
    reddit_service_works = test_reddit_service_directly()
    
    # Test full integration
    integration_works = test_reddit_reviews_integration()
    
    print("\n" + "="*60)
    print("🎯 TEST RESULTS:")
    print(f"Reddit Service: {'✅ Working' if reddit_service_works else '❌ Failed'}")
    print(f"Email Integration: {'✅ Working' if integration_works else '❌ Failed'}")
    
    if reddit_service_works and integration_works:
        print("\n🎉 Reddit reviews are successfully integrated!")
        print("📧 Users will now receive Reddit customer experiences in their emails")
    else:
        print("\n⚠️ Some issues detected - check output above for details")
