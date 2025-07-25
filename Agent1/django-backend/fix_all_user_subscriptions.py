#!/usr/bin/env python
"""
Fix ALL subscriptions for the user's email - clean up fake timestamps
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

def fix_all_user_subscriptions():
    """Fix ALL subscriptions for the user's email address"""
    
    print("🔧 Fixing ALL subscriptions for t-tokelowo@microsoft.com...")
    
    # Get ALL subscriptions for the user
    user_subscriptions = ReportSubscription.objects.filter(
        user_email="t-tokelowo@microsoft.com", 
        is_active=True
    )
    
    if not user_subscriptions.exists():
        print("❌ No subscriptions found for t-tokelowo@microsoft.com!")
        return False
    
    current_time = timezone.now()
    print(f"🕐 Current time: {current_time}")
    print(f"📧 Found {user_subscriptions.count()} subscriptions to fix:")
    
    for subscription in user_subscriptions:
        print(f"\n📋 Subscription: {subscription.agent_type}")
        print(f"   Old last_run_date: {subscription.last_run_date}")
        print(f"   Old next_run_date: {subscription.next_run_date}")
        
        # Reset the fake timestamps
        subscription.last_run_date = None  # Clear the fake timestamp
        subscription.next_run_date = current_time - timedelta(hours=1)  # Make it due now
        subscription.save()
        
        print(f"   ✅ Fixed last_run_date: {subscription.last_run_date}")
        print(f"   ✅ Fixed next_run_date: {subscription.next_run_date}")
    
    print(f"\n🎉 Fixed {user_subscriptions.count()} subscriptions!")
    print("🚀 All subscriptions are now due for delivery with clean timestamps!")
    
    return True

if __name__ == "__main__":
    fix_all_user_subscriptions()
