#!/usr/bin/env python
"""
Check and use the actual timezone stored in subscriptions
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

def check_subscription_timezones():
    """Check what timezones are actually stored in subscriptions"""
    
    print("🔧 Checking actual subscription timezones...")
    
    # Get user subscriptions
    user_subscriptions = ReportSubscription.objects.filter(
        user_email="t-tokelowo@microsoft.com", 
        is_active=True
    )
    
    if not user_subscriptions.exists():
        print("❌ No subscriptions found!")
        return False
    
    print(f"📋 Found {user_subscriptions.count()} subscriptions:")
    
    for i, subscription in enumerate(user_subscriptions, 1):
        print(f"\n{i}. {subscription.agent_type}")
        print(f"   Email: {subscription.user_email}")
        print(f"   Timezone: {subscription.time_zone}")  # This is the actual timezone stored
        print(f"   Frequency: {subscription.frequency}")
        print(f"   Preferred time: {subscription.preferred_time}")
        print(f"   Next run date: {subscription.next_run_date}")
        print(f"   Last sent: {subscription.last_run_date}")
        
        # Calculate next delivery using the subscription's actual timezone
        if subscription.time_zone:
            try:
                user_tz = pytz.timezone(subscription.time_zone)
                current_time_user_tz = timezone.now().astimezone(user_tz)
                
                # Create next delivery time using subscription's timezone and preferred_time
                if subscription.preferred_time:
                    delivery_hour = subscription.preferred_time.hour
                    delivery_minute = subscription.preferred_time.minute
                else:
                    delivery_hour = 9  # Default to 9 AM
                    delivery_minute = 0
                
                # Calculate tomorrow at the specified delivery time in user's timezone
                tomorrow_delivery = current_time_user_tz.replace(
                    hour=delivery_hour, 
                    minute=delivery_minute, 
                    second=0, 
                    microsecond=0
                ) + timedelta(days=1)
                
                # Convert to UTC for storage
                tomorrow_delivery_utc = tomorrow_delivery.astimezone(pytz.UTC)
                
                print(f"   📅 Current time in {subscription.time_zone}: {current_time_user_tz}")
                print(f"   🎯 Should deliver at: {tomorrow_delivery} ({subscription.time_zone})")
                print(f"   🎯 In UTC: {tomorrow_delivery_utc}")
                
                # Update the subscription with correct timing
                subscription.next_run_date = tomorrow_delivery_utc
                subscription.save()
                
                print(f"   ✅ Updated next_run_date to use subscription's timezone!")
                
            except Exception as e:
                print(f"   ❌ Error with timezone {subscription.time_zone}: {str(e)}")
        else:
            print(f"   ⚠️  No timezone set in subscription!")
    
    return True

if __name__ == "__main__":
    check_subscription_timezones()
