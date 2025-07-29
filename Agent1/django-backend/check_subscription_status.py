#!/usr/bin/env python3
import sqlite3
import os
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.utils import timezone

def check_subscription_status():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    print("=== YOUR SUBSCRIPTION STATUS ===")
    cursor.execute('''
        SELECT user_email, agent_type, frequency, next_run_date, last_run_date, 
               is_active, preferred_time, time_zone, total_reports_sent
        FROM research_agent_reportsubscription 
        WHERE user_email = 't-tokelowo@microsoft.com'
    ''')
    
    subscriptions = cursor.fetchall()
    
    if not subscriptions:
        print("❌ No subscriptions found for t-tokelowo@microsoft.com")
    else:
        for sub in subscriptions:
            email, agent_type, frequency, next_run, last_run, active, pref_time, tz, total_sent = sub
            print(f"📧 Email: {email}")
            print(f"🤖 Agent: {agent_type}")
            print(f"⏰ Frequency: {frequency}")
            print(f"🟢 Active: {'Yes' if active else 'No'}")
            print(f"⏰ Preferred Time: {pref_time} ({tz})")
            print(f"📊 Total Reports Sent: {total_sent}")
            print(f"⏰ Next Run: {next_run}")
            print(f"⏰ Last Run: {last_run}")
            print("---")
    
    # Check current time
    current_time = timezone.now()
    print(f"🕒 Current Time: {current_time}")
    
    # Check if any subscriptions are due
    print("\n=== OVERDUE SUBSCRIPTIONS ===")
    cursor.execute('''
        SELECT user_email, agent_type, next_run_date, last_run_date
        FROM research_agent_reportsubscription 
        WHERE is_active = 1 AND next_run_date <= datetime('now')
    ''')
    
    overdue = cursor.fetchall()
    if not overdue:
        print("No overdue subscriptions")
    else:
        for sub in overdue:
            email, agent_type, next_run, last_run = sub
            print(f"📧 {email} - {agent_type}")
            print(f"   Should have run: {next_run}")
            print(f"   Last ran: {last_run}")
    
    conn.close()

if __name__ == "__main__":
    check_subscription_status()
