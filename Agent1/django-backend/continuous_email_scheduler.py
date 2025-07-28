#!/usr/bin/env python
"""
Continuous email scheduler that runs in the background
Alternative to Windows Task Scheduler - keeps running and checks every hour
"""
import os
import sys
import django
import time
import schedule
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.management import call_command

def send_scheduled_emails():
    """Function to send scheduled emails"""
    try:
        print(f"\n🔄 Checking for due email subscriptions at {datetime.now()}")
        call_command('send_scheduled_reports')
        print(f"✅ Email check completed at {datetime.now()}")
    except Exception as e:
        print(f"❌ Error sending emails: {str(e)}")

def run_continuous_scheduler():
    """Run the email scheduler continuously"""
    print("🚀 Starting continuous email scheduler...")
    print("📧 Will check for due emails every day at 9:00 AM")
    print("⏹️  Press Ctrl+C to stop")
    
    # Schedule daily emails at 9:00 AM
    schedule.every().day.at("09:00").do(send_scheduled_emails)
    
    # Also check every hour in case we missed the exact time
    schedule.every().hour.do(send_scheduled_emails)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n🛑 Email scheduler stopped by user")

if __name__ == "__main__":
    run_continuous_scheduler()
