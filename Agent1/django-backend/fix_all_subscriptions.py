#!/usr/bin/env python
"""
Fix ALL subscriptions for t-tokelowo@microsoft.com to have correct timestamps
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

def fix_all_subscriptions():
    """Update ALL subscriptions for t-tokelowo@microsoft.com"""
    
    print("🔧 Finding ALL subscriptions for t-tokelowo@microsoft.com...")
    
    # Get ALL subscriptions for your email
    subscriptions = ReportSubscription.objects.filter(
        user_email="t-tokelowo@microsoft.com",
        is_active=True
    )
    
    print(f"📧 Found {subscriptions.count()} subscriptions for t-tokelowo@microsoft.com")
    
    for subscription in subscriptions:
        print(f"\n--- Fixing subscription {subscription.id} ---")
        print(f"Type: {subscription.get_agent_type_display()}")
        print(f"OLD Last sent: {subscription.last_run_date}")
        print(f"OLD Next run: {subscription.next_run_date}")
        
        # Update both timestamps correctly
        subscription.last_run_date = timezone.now()
        subscription.next_run_date = timezone.now() + timedelta(days=1)  # Tomorrow at same time
        subscription.save()
        
        print(f"NEW Last sent: {subscription.last_run_date}")
        print(f"NEW Next run: {subscription.next_run_date}")
        print("✅ FIXED!")
    
    print(f"\n🎉 Fixed {subscriptions.count()} subscriptions!")
    return True

if __name__ == "__main__":
    fix_all_subscriptions()
