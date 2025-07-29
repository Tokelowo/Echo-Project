#!/usr/bin/env python
"""
Fix both subscriptions to use PST timezone as requested by user
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.models import ReportSubscription
from django.utils import timezone
import pytz

def fix_to_pst_timezone():
    """Fix both subscriptions to use PST timezone"""
    
    print("🔧 Fixing both subscriptions to use PST timezone...")
    
    # Get user subscriptions
    user_subscriptions = ReportSubscription.objects.filter(
        user_email="t-tokelowo@microsoft.com", 
        is_active=True
    )
    
    if not user_subscriptions.exists():
        print("❌ No subscriptions found!")
        return False
    
    # Set PST timezone
    pst_tz = pytz.timezone('US/Pacific')
    current_pst = timezone.now().astimezone(pst_tz)
    
    print(f"🕐 Current PST time: {current_pst}")
    print(f"📋 Updating {user_subscriptions.count()} subscriptions to PST:")
    
    for i, subscription in enumerate(user_subscriptions, 1):
        print(f"\n{i}. {subscription.agent_type}")
        print(f"   Old timezone: {subscription.time_zone}")
        print(f"   Old preferred_time: {subscription.preferred_time}")
        print(f"   Old next_run_date: {subscription.next_run_date}")
        
        # Update to PST timezone
        subscription.time_zone = 'US/Pacific'
        
        # Calculate tomorrow 9:00 AM PST
        tomorrow_9am_pst = current_pst.replace(
            hour=9, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)
        
        # Convert to UTC for storage
        tomorrow_9am_utc = tomorrow_9am_pst.astimezone(pytz.UTC)
        
        subscription.next_run_date = tomorrow_9am_utc
        subscription.save()
        
        print(f"   ✅ New timezone: {subscription.time_zone}")
        print(f"   ✅ New preferred_time: {subscription.preferred_time}")
        print(f"   ✅ New next_run_date: {subscription.next_run_date}")
        print(f"   🎯 Will deliver tomorrow at 9:00 AM PST")
        print(f"   🎯 PST time: {tomorrow_9am_pst}")
    
    hours_until = (tomorrow_9am_utc - timezone.now()).total_seconds() / 3600
    print(f"\n⏰ FINAL SCHEDULE:")
    print(f"   Both subscriptions now use PST timezone")
    print(f"   Delivery: Tomorrow 9:00 AM PST")
    print(f"   Hours until delivery: {hours_until:.1f}")
    
    return True

if __name__ == "__main__":
    fix_to_pst_timezone()
