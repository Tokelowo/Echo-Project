#!/usr/bin/env python
"""
IMMEDIATE EMAIL TEST - Send right now to verify system works
"""
import os
import django
import sys

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def send_immediate_test_email():
    print("📧 SENDING IMMEDIATE TEST EMAIL...")
    
    try:
        from research_agent.enhanced_email_service import EnhancedEmailService
        from research_agent.research_coordinator import ResearchCoordinator
        from datetime import datetime
        
        # Create sample report data
        report_data = {
            'title': '🚨 URGENT: Email System Restored!',
            'summary': 'Your daily email system has been successfully restored and is now working.',
            'sections': [
                {
                    'title': '✅ System Status',
                    'content': 'The email delivery system has been fixed and restored to full functionality.'
                },
                {
                    'title': '📅 Schedule',
                    'content': 'Daily emails will now be delivered every morning at 9:00 AM as requested.'
                },
                {
                    'title': '🔧 What Was Fixed',
                    'content': 'Recreated email subscription, set up Windows scheduled task, and verified email pipeline.'
                }
            ],
            'generated_at': datetime.now(),
            'agent_type': 'System Restoration',
            'user_email': 'Temiloluwaokelowo@gmail.com',
            'user_name': 'Temiloluwa'
        }
        
        # Send the email
        email_service = EnhancedEmailService()
        result = email_service.send_professional_report_email(
            report_data=report_data,
            recipient_email='Temiloluwaokelowo@gmail.com',
            recipient_name='Temiloluwa'
        )
        
        if result.get('success'):
            print("🎉 SUCCESS! Test email sent successfully!")
            print(f"📧 Sent to: Temiloluwaokelowo@gmail.com")
            print("📱 Check your inbox - email should arrive within a few minutes.")
        else:
            print(f"❌ Failed to send email: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error sending test email: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    send_immediate_test_email()
