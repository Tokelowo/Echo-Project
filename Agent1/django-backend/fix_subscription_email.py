#!/usr/bin/env python
"""
Fix subscription email address to use correct recipient
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.models import ReportSubscription
from django.utils import timezone

def fix_subscription_email():
    """Update subscription to use correct email address"""
    
    print("🔧 Fixing subscription email address...")
    
    # Get the active subscription
    subscription = ReportSubscription.objects.filter(is_active=True).first()
    if not subscription:
        print("❌ No active subscription found!")
        return False
        
    print(f"📧 Current subscription email: {subscription.user_email}")
    
    # Update to correct email address  
    subscription.user_email = "t-tokelowo@microsoft.com"
    subscription.user_name = "Temiloluwa Okelowo"
    subscription.save()
    
    print(f"✅ Updated subscription email to: {subscription.user_email}")
    print(f"✅ Updated subscription name to: {subscription.user_name}")
    
    return True

if __name__ == "__main__":
    fix_subscription_email()
