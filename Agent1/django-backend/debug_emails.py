#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from research_agent.models import ReportSubscription
from django.utils import timezone

def check_email_status():
    print("=== EMAIL SUBSCRIPTION STATUS ===")
    print(f"Current time: {timezone.now()}")
    
    try:
        # Get all subscriptions
        subscriptions = ReportSubscription.objects.all()
        print(f"Total subscriptions found: {subscriptions.count()}")
        
        if subscriptions.count() == 0:
            print("❌ NO SUBSCRIPTIONS FOUND! This is the problem.")
            return
        
        for sub in subscriptions:
            print(f"\n📧 Email: {sub.user_email}")
            print(f"   Active: {sub.is_active}")
            print(f"   Agent Type: {sub.agent_type}")
            print(f"   Preferred Time: {sub.preferred_time}")
            print(f"   Next Run Date: {sub.next_run_date}")
            print(f"   Created: {sub.created_at}")
            
            # Check if this subscription is due
            if sub.is_active and sub.next_run_date:
                is_due = sub.next_run_date <= timezone.now()
                print(f"   Due now: {'✅ YES' if is_due else '❌ NO'}")
            else:
                print(f"   Due now: ❌ NOT ACTIVE OR NO NEXT RUN DATE")
                
    except Exception as e:
        print(f"❌ Error accessing subscriptions: {e}")

if __name__ == "__main__":
    check_email_status()
