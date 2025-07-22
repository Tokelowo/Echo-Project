#!/usr/bin/env python
import os
import django
import sys
from datetime import datetime, time, timedelta

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from research_agent.models import ReportSubscription
from django.utils import timezone

def fix_email_subscription():
    print("=== FIXING EMAIL SUBSCRIPTION ===")
    
    # Your email addresses
    email_addresses = ['Temiloluwaokelowo@gmail.com', 't-tokelowo@microsoft.com']
    
    for email in email_addresses:
        # Check if subscription exists
        existing = ReportSubscription.objects.filter(user_email=email, is_active=True).first()
        
        if existing:
            print(f"✅ Found existing subscription for {email}")
            print(f"   Next run: {existing.next_run_date}")
            
            # Update the next run date to tomorrow at 9 AM
            tomorrow_9am = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
            existing.next_run_date = tomorrow_9am
            existing.preferred_time = time(9, 0)
            existing.save()
            print(f"   Updated next run to: {tomorrow_9am}")
            
        else:
            print(f"❌ No active subscription found for {email}")
            print(f"   Creating new subscription...")
            
            # Create new subscription
            subscription = ReportSubscription.objects.create(
                user_email=email,
                user_name=email.split('@')[0],
                agent_type='market_intelligence',
                frequency='daily',
                preferred_time=time(9, 0),
                time_zone='UTC',
                is_active=True,
                query_template='Generate a comprehensive daily market intelligence report',
                focus_areas='technology,market trends,competitive analysis',
                delivery_format='email_html',
                next_run_date=timezone.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
            )
            print(f"   ✅ Created subscription with ID: {subscription.id}")
            print(f"   Next run: {subscription.next_run_date}")

    print("\n=== VERIFICATION ===")
    active_subs = ReportSubscription.objects.filter(is_active=True)
    print(f"Total active subscriptions: {active_subs.count()}")
    
    for sub in active_subs:
        print(f"📧 {sub.user_email} -> Next delivery: {sub.next_run_date}")

if __name__ == "__main__":
    fix_email_subscription()
