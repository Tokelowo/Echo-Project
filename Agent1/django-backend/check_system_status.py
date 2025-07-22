#!/usr/bin/env python
"""
EMAIL SYSTEM STATUS CHECK
"""
import os
import django
import sys

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.models import ReportSubscription
from django.utils import timezone
from datetime import datetime

def check_system_status():
    print("📊 EMAIL SYSTEM STATUS REPORT")
    print("=" * 50)
    print(f"🕐 Current time: {timezone.now()}")
    print(f"📅 Current date: {timezone.now().date()}")
    
    # Check subscriptions
    print(f"\n📧 EMAIL SUBSCRIPTIONS:")
    subscriptions = ReportSubscription.objects.filter(is_active=True)
    print(f"   Active subscriptions: {subscriptions.count()}")
    
    if subscriptions.count() == 0:
        print("   ❌ NO ACTIVE SUBSCRIPTIONS FOUND!")
        return
        
    for sub in subscriptions:
        print(f"\n   📬 Email: {sub.user_email}")
        print(f"      Type: {sub.agent_type}")
        print(f"      Frequency: {sub.frequency}")
        print(f"      Preferred time: {sub.preferred_time}")
        print(f"      Next delivery: {sub.next_run_date}")
        print(f"      Active: {'✅ YES' if sub.is_active else '❌ NO'}")
        
        # Check if due
        if sub.next_run_date:
            is_due = sub.next_run_date <= timezone.now()
            print(f"      Due now: {'✅ YES' if is_due else '❌ NO'}")
        else:
            print(f"      Due now: ❌ NO SCHEDULE SET")
    
    # Check if files exist
    print(f"\n📁 FILE STATUS:")
    batch_file = "send_daily_emails.bat"
    print(f"   Batch file: {'✅ EXISTS' if os.path.exists(batch_file) else '❌ MISSING'}")
    
    # Check Windows scheduled task
    print(f"\n⏰ SCHEDULED TASK STATUS:")
    try:
        import subprocess
        result = subprocess.run(['schtasks', '/query', '/tn', 'DailyEmailReports'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Windows scheduled task exists")
        else:
            print("   ❌ Windows scheduled task not found")
    except:
        print("   ⚠️ Could not check Windows scheduled task")
    
    print(f"\n🎯 SUMMARY:")
    if subscriptions.count() > 0:
        print("   ✅ Email subscriptions are configured")
        print("   ✅ System should be working")
        print("   📅 Next email will be sent at scheduled time")
    else:
        print("   ❌ No email subscriptions found")
        print("   🔧 System needs to be reconfigured")

if __name__ == "__main__":
    check_system_status()
