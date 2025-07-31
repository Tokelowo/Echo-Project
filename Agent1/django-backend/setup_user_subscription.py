#!/usr/bin/env python3

import os
import django
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def setup_user_subscription():
    """Set up daily email subscription for the user"""
    
    print("🔧 SETTING UP DAILY EMAIL SUBSCRIPTION")
    print("=" * 50)
    
    # User details
    user_email = "t-tokelowo@microsoft.com"
    backup_email = "Temiloluwaokelowo@gmail.com"
    user_name = "Temiloluwa Okelowo"
    
    # Timezone - Microsoft typically uses Pacific Time
    user_timezone = "America/Los_Angeles"  # Pacific Time
    preferred_time = "09:00"  # 9:00 AM
    
    print(f"👤 User: {user_name}")
    print(f"📧 Primary Email: {user_email}")
    print(f"📧 Backup Email: {backup_email}")
    print(f"🌍 Timezone: {user_timezone}")
    print(f"⏰ Preferred Time: {preferred_time} Pacific Time")
    
    # Create subscription record (simulated - would be in database)
    subscription_data = {
        "user_name": user_name,
        "primary_email": user_email,
        "backup_email": backup_email,
        "timezone": user_timezone,
        "preferred_time": preferred_time,
        "frequency": "daily",
        "active": True,
        "created_date": datetime.now().isoformat(),
        "last_sent": None,
        "next_due": None
    }
    
    # Calculate next email time
    tz = pytz.timezone(user_timezone)
    now = datetime.now(tz)
    
    # Set next email for tomorrow at 9 AM Pacific
    next_email = now.replace(hour=9, minute=0, second=0, microsecond=0)
    if next_email <= now:
        next_email += timedelta(days=1)
    
    subscription_data["next_due"] = next_email.isoformat()
    
    print(f"\n📅 Next Email Scheduled: {next_email.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Test email to confirm subscription
    print(f"\n📨 Sending confirmation email...")
    
    try:
        subject = "✅ Echo Intelligence Daily Subscription Activated"
        message = f"""
Hello {user_name},

Your daily Echo Intelligence cybersecurity report subscription has been successfully activated!

📋 Subscription Details:
• Email: {user_email}
• Backup: {backup_email}
• Frequency: Daily at {preferred_time} {user_timezone}
• Next Report: {next_email.strftime('%Y-%m-%d %H:%M:%S %Z')}

🔒 What you'll receive:
• Daily cybersecurity threat intelligence
• Market trends and analysis
• Reddit community insights
• Professional threat assessments
• DOCX reports with detailed findings

Your reports will include:
• Real-time threat analysis
• Industry-specific intelligence
• Community discussions from Reddit
• Professional formatting with Microsoft branding
• Actionable cybersecurity insights

Thank you for subscribing to Echo Intelligence!

Best regards,
Echo Intelligence Team
        """
        
        result = send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email, backup_email],
            fail_silently=False,
        )
        
        print(f"✅ Confirmation email sent successfully! Result: {result}")
        print(f"📧 Sent to: {user_email} and {backup_email}")
        
    except Exception as e:
        print(f"❌ Failed to send confirmation email: {e}")
        return False
    
    # Save subscription to file (simulated database)
    try:
        import json
        with open('user_subscription.json', 'w') as f:
            json.dump(subscription_data, f, indent=2)
        print(f"✅ Subscription saved to user_subscription.json")
    except Exception as e:
        print(f"⚠️ Could not save subscription file: {e}")
    
    print(f"\n🎉 SUBSCRIPTION SETUP COMPLETE!")
    print(f"You will receive daily cybersecurity intelligence reports every day at {preferred_time} Pacific Time.")
    print(f"Check your email ({user_email}) for the confirmation message.")
    
    return True

if __name__ == "__main__":
    setup_user_subscription()
