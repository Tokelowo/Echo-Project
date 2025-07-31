#!/usr/bin/env python
"""
Quick fix for email sending - uses correct function names
"""
import os
import sys
import django

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def send_todays_email():
    """Send today's email using the correct function"""
    try:
        from research_agent.enhanced_email_service import EnhancedEmailService
        from research_agent.models import EmailSubscription
        from research_agent.views import generate_comprehensive_intelligence_report
        
        print("📧 Sending today's email...")
        
        # Get active subscriptions
        subscriptions = EmailSubscription.objects.filter(is_active=True)
        print(f"Found {subscriptions.count()} active subscriptions")
        
        if not subscriptions.exists():
            print("❌ No active subscriptions found")
            return
        
        # Generate report data
        print("📊 Generating report data...")
        report_data = generate_comprehensive_intelligence_report()
        
        # Initialize email service
        email_service = EnhancedEmailService()
        
        # Send to each subscription
        for subscription in subscriptions:
            print(f"📧 Sending to {subscription.email}...")
            
            try:
                # Use the correct method name
                result = email_service.send_enhanced_report_email(
                    report_data=report_data,
                    recipient_email=subscription.email,
                    recipient_name=subscription.name or 'Valued Subscriber'
                )
                
                if result.get('success'):
                    print(f"✅ Email sent successfully to {subscription.email}")
                    subscription.last_email_sent = timezone.now()
                    subscription.save()
                else:
                    print(f"❌ Failed to send email to {subscription.email}: {result.get('error')}")
                    
            except Exception as e:
                print(f"❌ Error sending to {subscription.email}: {str(e)}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    send_todays_email()
