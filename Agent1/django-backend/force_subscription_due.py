#!/usr/bin/env python
"""
Force subscription to be due for testing
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

def force_subscription_due():
    """Set subscription to be due for immediate delivery"""
    
    print("🔧 Setting subscription to be due for delivery...")
    
    # Get the active subscription
    subscription = ReportSubscription.objects.filter(is_active=True).first()
    if not subscription:
        print("❌ No active subscription found!")
        return False
        
    print(f"📧 Current subscription: {subscription.user_email}")
    print(f"📅 Current next_run_date: {subscription.next_run_date}")
    
    # Set next_run_date to 1 hour ago to make it due
    subscription.next_run_date = timezone.now() - timedelta(hours=1)
    subscription.save()
    
    print(f"✅ Updated next_run_date to: {subscription.next_run_date}")
    print("🚀 Subscription is now due for delivery!")
    
    return True

if __name__ == "__main__":
    force_subscription_due()
