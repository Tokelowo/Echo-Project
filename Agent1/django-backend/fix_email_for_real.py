#!/usr/bin/env python
import os
import django
import sys
from datetime import datetime, time, timedelta

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.models import ReportSubscription
from django.utils import timezone

def setup_working_email_subscription():
    print("🔧 SETTING UP WORKING EMAIL SUBSCRIPTION...")
    
    email = 'Temiloluwaokelowo@gmail.com'
    
    # Remove any existing subscriptions
    old_subs = ReportSubscription.objects.filter(user_email=email)
    if old_subs.exists():
        print(f"Removing {old_subs.count()} old subscriptions...")
        old_subs.delete()
    
    # Calculate next 9 AM
    now = timezone.now()
    tomorrow_9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
    if tomorrow_9am <= now:
        tomorrow_9am += timedelta(days=1)
    
    # Create subscription due in 1 minute for immediate test
    test_sub = ReportSubscription.objects.create(
        user_email=email,
        user_name='Temiloluwa',
        agent_type='market_intelligence',
        frequency='daily',
        preferred_time=time(9, 0),
        time_zone='UTC',
        is_active=True,
        query_template='Generate a comprehensive daily business intelligence report',
        focus_areas='AI,technology,market trends,business intelligence',
        delivery_format='email_html',
        next_run_date=now + timedelta(minutes=1)
    )
    
    # Create subscription for daily 9 AM delivery
    daily_sub = ReportSubscription.objects.create(
        user_email=email,
        user_name='Temiloluwa',
        agent_type='market_intelligence',
        frequency='daily',
        preferred_time=time(9, 0),
        time_zone='UTC',
        is_active=True,
        query_template='Generate a comprehensive daily business intelligence report',
        focus_areas='AI,technology,market trends,business intelligence',
        delivery_format='email_html',
        next_run_date=tomorrow_9am
    )
    
    print(f"✅ Created test subscription (ID: {test_sub.id}) - due in 1 minute")
    print(f"✅ Created daily subscription (ID: {daily_sub.id}) - due at {tomorrow_9am}")
    
    return test_sub, daily_sub

def test_immediate_send():
    print("\n⚡ TESTING IMMEDIATE SEND...")
    
    from django.core.management import call_command
    from io import StringIO
    import sys
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        call_command('send_scheduled_reports', verbosity=2)
        output = mystdout.getvalue()
        sys.stdout = old_stdout
        
        print("Command output:")
        print(output)
        
        if "Sent" in output or "sent" in output:
            print("🎉 EMAIL SENT SUCCESSFULLY!")
            return True
        else:
            print("⚠️ No emails were sent. Output above shows details.")
            return False
            
    except Exception as e:
        sys.stdout = old_stdout
        print(f"❌ Error running send command: {e}")
        return False

if __name__ == "__main__":
    print("🚨 FIXING YOUR EMAIL SYSTEM - FOR REAL THIS TIME!")
    print("=" * 60)
    
    # Step 1: Set up subscriptions
    test_sub, daily_sub = setup_working_email_subscription()
    
    # Step 2: Test immediate send
    success = test_immediate_send()
    
    if success:
        print("\n🎉 SUCCESS! Your email system is working!")
        print("📧 You should receive an email shortly.")
        print("📅 Daily emails will be sent every morning at 9:00 AM.")
    else:
        print("\n⚠️ Email system configured but may need manual testing.")
        print("🔧 Run this to test manually:")
        print("   python manage.py send_scheduled_reports")
    
    print(f"\n📊 Summary:")
    print(f"   Test subscription ID: {test_sub.id}")
    print(f"   Daily subscription ID: {daily_sub.id}")
    print(f"   Next daily email: {daily_sub.next_run_date}")
