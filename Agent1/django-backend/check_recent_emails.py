#!/usr/bin/env python3
import sqlite3
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def check_email_deliveries():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Check recent email deliveries
    cursor.execute('''
        SELECT id, recipient_email, status, sent_at, error_message, subject
        FROM research_agent_emaildelivery 
        ORDER BY sent_at DESC 
        LIMIT 20
    ''')
    
    results = cursor.fetchall()
    
    print("=== RECENT EMAIL DELIVERIES ===")
    if not results:
        print("No email deliveries found in database")
    else:
        for row in results:
            id_val, email, status, sent_at, error, subject = row
            print(f"ID: {id_val}")
            print(f"Email: {email}")
            print(f"Status: {status}")
            print(f"Sent: {sent_at}")
            print(f"Subject: {subject}")
            print(f"Error: {error if error else 'None'}")
            print("---")
    
    # Check for your specific email
    print("\n=== YOUR EMAIL DELIVERIES (t-tokelowo@microsoft.com) ===")
    cursor.execute('''
        SELECT id, status, sent_at, error_message, subject
        FROM research_agent_emaildelivery 
        WHERE recipient_email = 't-tokelowo@microsoft.com'
        ORDER BY sent_at DESC 
        LIMIT 10
    ''')
    
    your_emails = cursor.fetchall()
    if not your_emails:
        print("No email deliveries found for t-tokelowo@microsoft.com")
    else:
        for row in your_emails:
            id_val, status, sent_at, error, subject = row
            print(f"ID: {id_val}, Status: {status}, Sent: {sent_at}")
            print(f"Subject: {subject}")
            print(f"Error: {error if error else 'None'}")
            print("---")
    
    # Check for failed deliveries today
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n=== FAILED DELIVERIES TODAY ({today}) ===")
    cursor.execute('''
        SELECT recipient_email, status, sent_at, error_message, subject
        FROM research_agent_emaildelivery 
        WHERE status = 'failed' AND DATE(sent_at) = ?
        ORDER BY sent_at DESC
    ''', (today,))
    
    failed_today = cursor.fetchall()
    if not failed_today:
        print("No failed deliveries today")
    else:
        for row in failed_today:
            email, status, sent_at, error, subject = row
            print(f"Email: {email}, Status: {status}")
            print(f"Sent: {sent_at}")
            print(f"Subject: {subject}")
            print(f"Error: {error}")
            print("---")
    
    conn.close()

if __name__ == "__main__":
    check_email_deliveries()
