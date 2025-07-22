#!/usr/bin/env python3
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.models import ReportSubscription
from django.utils import timezone

def check_subscriptions():
    print("=== EMAIL SUBSCRIPTION STATUS ===")
    
    # Get all subscriptions
    all_subs = ReportSubscription.objects.all()
    active_subs = ReportSubscription.objects.filter(is_active=True)
    
    print(f"Total subscriptions: {all_subs.count()}")
    print(f"Active subscriptions: {active_subs.count()}")
    
    if active_subs.exists():
        print("\nACTIVE SUBSCRIPTIONS:")
        print("-" * 50)
        for sub in active_subs:
            print(f"Email: {sub.user_email}")
            print(f"Type: {sub.get_agent_type_display()}")
            print(f"Frequency: {sub.frequency}")
            print(f"Next delivery: {sub.next_run_date}")
            print(f"Last sent: {sub.last_run_date}")
            print("-" * 30)
    else:
        print("\nNo active subscriptions found.")
        print("You may need to subscribe to daily emails through the web app.")
    
    # Check for due subscriptions
    now = timezone.now()
    due_subs = active_subs.filter(next_run_date__lte=now)
    
    print(f"\nSubscriptions due now: {due_subs.count()}")
    if due_subs.exists():
        print("Due subscriptions:")
        for sub in due_subs:
            print(f"  - {sub.user_email} ({sub.get_agent_type_display()})")

if __name__ == "__main__":
    check_subscriptions()
