#!/usr/bin/env python3
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.models import ReportSubscription
from django.utils import timezone
from datetime import datetime, timedelta

def create_daily_subscription():
    """Create a daily email subscription for testing"""
    
    email = input("Enter your email address: ").strip()
    if not email:
        print("Email address is required!")
        return
    
    name = input("Enter your name (optional): ").strip() or "Daily Subscriber"
    
    # Create subscription
    subscription = ReportSubscription.objects.create(
        user_email=email,
        user_name=name,
        agent_type='comprehensive_research',  # Multi-agent research
        frequency='daily',
        preferred_time='09:00',  # 9 AM
        time_zone='America/New_York',  # Adjust as needed
        is_active=True,
        focus_areas=['Market Intelligence', 'Threat Analysis', 'Competitive Insights'],
        delivery_format='email',
        query_template='Generate a comprehensive daily intelligence briefing with market trends, competitive analysis, and security insights for Microsoft Defender for Office 365'
    )
    
    print(f"✅ Created daily subscription for {email}")
    print(f"   - Type: {subscription.get_agent_type_display()}")
    print(f"   - Frequency: {subscription.frequency}")
    print(f"   - Time: {subscription.preferred_time} {subscription.time_zone}")
    print(f"   - Next delivery: {subscription.get_next_delivery_local_time()}")
    print(f"   - Subscription ID: {subscription.id}")
    
    return subscription

if __name__ == "__main__":
    print("=== DAILY EMAIL SUBSCRIPTION SETUP ===")
    create_daily_subscription()
