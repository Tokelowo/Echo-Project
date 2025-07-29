#!/usr/bin/env python
"""
Force ALL user subscriptions to be due for testing
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

def force_all_user_subscriptions_due():
    """Set all user subscriptions to be due for immediate delivery"""
    
    print("🔧 Setting all user subscriptions to be due for delivery...")
    
    # Get user subscriptions
    user_subscriptions = ReportSubscription.objects.filter(
        user_email="t-tokelowo@microsoft.com", 
        is_active=True
    )
    
    if not user_subscriptions.exists():
        print("❌ No subscriptions found!")
        return False
    
    for subscription in user_subscriptions:
        print(f"📧 Subscription: {subscription.agent_type}")
        print(f"📅 Old next_run_date: {subscription.next_run_date}")
        
        # Set next_run_date to 1 hour ago to make it due
        subscription.next_run_date = timezone.now() - timedelta(hours=1)
        subscription.save()
        
        print(f"✅ Updated next_run_date to: {subscription.next_run_date}")
    
    print(f"🚀 All {user_subscriptions.count()} subscriptions are now due for delivery!")
    
    return True

if __name__ == "__main__":
    force_all_user_subscriptions_due()
