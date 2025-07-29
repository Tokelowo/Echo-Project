#!/usr/bin/env python
"""
Fix delivery schedule for PST timezone
"""
import os
import sys
import django
from datetime import datetime, timedelta
import pytz

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.models import ReportSubscription
from django.utils import timezone

def fix_pst_delivery_schedule():
    """Fix delivery schedule for PST timezone"""
    
    print("🔧 Fixing delivery schedule for PST timezone...")
    
    # Get user subscriptions
    user_subscriptions = ReportSubscription.objects.filter(
        user_email="t-tokelowo@microsoft.com", 
        is_active=True
    )
    
    if not user_subscriptions.exists():
        print("❌ No subscriptions found!")
        return False
    
    # Set PST timezone
    pst = pytz.timezone('US/Pacific')
    current_time_pst = timezone.now().astimezone(pst)
    
    # Set delivery for tomorrow 9:00 AM PST
    tomorrow_9am_pst = current_time_pst.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
    tomorrow_9am_utc = tomorrow_9am_pst.astimezone(pytz.UTC)
    
    print(f"🕐 Current PST time: {current_time_pst}")
    print(f"📅 Target delivery: Tomorrow 9:00 AM PST = {tomorrow_9am_pst}")
    print(f"📅 In UTC: {tomorrow_9am_utc}")
    
    for subscription in user_subscriptions:
        print(f"\n📋 Updating {subscription.agent_type}:")
        print(f"   Old next_run_date: {subscription.next_run_date}")
        
        subscription.next_run_date = tomorrow_9am_utc
        subscription.save()
        
        print(f"   ✅ New next_run_date: {subscription.next_run_date}")
        print(f"   🎯 Will deliver at 9:00 AM PST tomorrow!")
    
    hours_until = (tomorrow_9am_utc - timezone.now()).total_seconds() / 3600
    print(f"\n⏰ DELIVERY SCHEDULE:")
    print(f"   Hours until delivery: {hours_until:.1f}")
    print(f"   Tomorrow 9:00 AM PST = {tomorrow_9am_pst.strftime('%Y-%m-%d %I:%M %p PST')}")
    print(f"   (That's {tomorrow_9am_utc.strftime('%Y-%m-%d %H:%M:%S UTC')} in server time)")
    
    return True

if __name__ == "__main__":
    fix_pst_delivery_schedule()
