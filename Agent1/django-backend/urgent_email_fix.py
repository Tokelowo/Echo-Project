#!/usr/bin/env python
"""
URGENT EMAIL FIX - Daily Email Restoration Script
"""
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

def urgent_email_fix():
    print("🚨 URGENT EMAIL FIX IN PROGRESS...")
    print(f"Time: {timezone.now()}")
    
    # Your email
    email = 'Temiloluwaokelowo@gmail.com'
    
    # Delete any existing subscriptions to start fresh
    old_subs = ReportSubscription.objects.filter(user_email=email)
    if old_subs.exists():
        print(f"Deleting {old_subs.count()} old subscriptions...")
        old_subs.delete()
    
    # Create a fresh subscription that's due NOW
    print("Creating fresh email subscription...")
    subscription = ReportSubscription.objects.create(
        user_email=email,
        user_name='Temiloluwa',
        agent_type='market_intelligence',
        frequency='daily', 
        preferred_time=time(9, 0),
        time_zone='UTC',
        is_active=True,
        query_template='Generate a comprehensive daily business intelligence report covering market trends, competitive analysis, and technology insights',
        focus_areas='AI,technology,market trends,business intelligence,competitive analysis',
        delivery_format='email_html',
        next_run_date=timezone.now() + timedelta(seconds=30)  # Send in 30 seconds
    )
    
    print(f"✅ Created subscription ID: {subscription.id}")
    print(f"📧 Email: {subscription.user_email}")
    print(f"⏰ Next delivery: {subscription.next_run_date}")
    print(f"🎯 Active: {subscription.is_active}")
    
    # Also create one for tomorrow morning at 9 AM
    tomorrow_9am = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
    tomorrow_sub = ReportSubscription.objects.create(
        user_email=email,
        user_name='Temiloluwa', 
        agent_type='market_intelligence',
        frequency='daily',
        preferred_time=time(9, 0),
        time_zone='UTC',
        is_active=True,
        query_template='Generate a comprehensive daily business intelligence report covering market trends, competitive analysis, and technology insights',
        focus_areas='AI,technology,market trends,business intelligence,competitive analysis',
        delivery_format='email_html',
        next_run_date=tomorrow_9am
    )
    
    print(f"✅ Also created tomorrow's subscription ID: {tomorrow_sub.id}")
    print(f"📅 Tomorrow's delivery: {tomorrow_sub.next_run_date}")
    
    print("\n🔧 EMAIL SYSTEM RESTORED!")
    print("You should receive an email in about 30 seconds, then daily at 9 AM.")
    
    return subscription

if __name__ == "__main__":
    subscription = urgent_email_fix()
    
    # Now try to send it immediately
    print("\n⚡ Attempting immediate send...")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('send_scheduled_reports', stdout=out, verbosity=2)
        output = out.getvalue()
        print("Send command output:")
        print(output)
        
        if "✓ Sent" in output:
            print("🎉 EMAIL SENT SUCCESSFULLY!")
        else:
            print("⚠️ Email may not have sent. Check the output above.")
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        import traceback
        traceback.print_exc()
