#!/usr/bin/env python
"""
Test real email delivery system - bypass subscription layer
"""
import os
import sys
import django
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.enhanced_email_service import EnhancedEmailService
from research_agent.models import ReportSubscription
from django.utils import timezone

def test_real_email_delivery():
    """Test if the email system actually sends emails"""
    
    print(f"🔧 Testing real email delivery at {timezone.now()}")
    
    # Get the active subscription
    try:
        subscription = ReportSubscription.objects.filter(is_active=True).first()
        if not subscription:
            print("❌ No active subscription found!")
            return False
            
        print(f"📧 Found subscription for: {subscription.user_email}")
        print(f"📅 Current time: {timezone.now()}")
        print(f"📅 Subscription last sent: {subscription.last_run_date}")
        
        # Create sample report data
        report_data = {
            'title': 'Comprehensive Multi-Agent Research Report',
            'summary': 'Real-time test of email delivery system',
            'articles': [
                {
                    'title': 'Test Article - Email Delivery Verification',
                    'url': 'https://example.com/test',
                    'description': 'This is a test to verify email delivery is working correctly.',
                    'source': 'Test Source'
                }
            ],
            'reddit_reviews': [
                {
                    'username': 'test_user',
                    'content': 'Testing Reddit integration in email delivery.',
                    'score': 5,
                    'replies': 2,
                    'url': 'https://reddit.com/test'
                }
            ],
            'microsoft_articles': [],
            'metadata': {
                'generated_at': timezone.now().isoformat(),
                'total_articles': 1,
                'agent_type': 'comprehensive'
            }
        }
        
        # Test direct email delivery using EnhancedEmailService
        email_service = EnhancedEmailService()
        
        print(f"📮 Sending test email to {subscription.user_email}...")
        
        result = email_service.send_professional_report_email(
            report_data, 
            subscription.user_email, 
            subscription.user_name
        )
        
        print(f"✅ Email delivery result: {result}")
        
        if result.get('status') == 'success':
            print(f"🎉 SUCCESS! Email was actually sent to {subscription.user_email}")
            
            # Update subscription timestamp correctly
            subscription.last_run_date = timezone.now()
            subscription.total_reports_sent += 1
            subscription.save()
            
            print(f"📊 Updated subscription - Last sent: {subscription.last_run_date}")
            return True
        else:
            print(f"❌ FAILED! Email delivery error: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"💥 ERROR during email test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_real_email_delivery()
    if success:
        print("\n✅ Email delivery system is working correctly!")
    else:
        print("\n❌ Email delivery system is NOT working!")
