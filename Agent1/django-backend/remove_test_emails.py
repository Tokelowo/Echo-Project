#!/usr/bin/env python3
"""
Remove test emails from subscription database
"""
import os
import sys
import django
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

try:
    django.setup()
except Exception as e:
    print(f"Django setup error: {e}")
    sys.exit(1)

from research_agent.models import ReportSubscription

def remove_test_emails():
    """Remove all test emails ending with @example.com"""
    try:
        # Find all test email subscriptions
        test_subscriptions = ReportSubscription.objects.filter(user_email__endswith='@example.com')
        
        print("=== REMOVING TEST EMAIL SUBSCRIPTIONS ===")
        print(f"Found {test_subscriptions.count()} test email subscriptions to remove:")
        
        # List what will be removed
        for subscription in test_subscriptions:
            print(f"  - {subscription.user_email} ({subscription.agent_type})")
        
        if test_subscriptions.count() > 0:
            # Remove the subscriptions
            deleted_count = test_subscriptions.delete()[0]
            print(f"\n✅ Successfully removed {deleted_count} test email subscriptions")
        else:
            print("\n✅ No test email subscriptions found to remove")
        
        # Show remaining subscriptions
        remaining = ReportSubscription.objects.all()
        print(f"\n=== REMAINING SUBSCRIPTIONS ({remaining.count()}) ===")
        for subscription in remaining:
            print(f"  - {subscription.user_email} ({subscription.agent_type}) - {subscription.frequency}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error removing test emails: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧹 Starting test email cleanup...")
    success = remove_test_emails()
    if success:
        print("\n🎉 Test email cleanup completed successfully!")
    else:
        print("\n💥 Test email cleanup failed!")
