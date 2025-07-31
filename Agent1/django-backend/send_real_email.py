import os
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=== SENDING YOUR DAILY EMAIL ===")
print(f"From: {settings.DEFAULT_FROM_EMAIL}")
print(f"To: t-tokelowo@microsoft.com")
print(f"Email Backend: {settings.EMAIL_BACKEND}")
print(f"SMTP Host: {settings.EMAIL_HOST}")

try:
    # Send actual email
    result = send_mail(
        subject="🛡️ Echo Intelligence - Daily Cybersecurity Report",
        message="""
        Daily Echo Intelligence Report
        
        Your comprehensive cybersecurity intelligence report is ready.
        
        Key highlights:
        • Market trends analysis
        • Threat landscape updates  
        • Competitive intelligence
        • Microsoft security updates
        
        This email confirms your daily subscription is active and working.
        
        Best regards,
        Echo Intelligence Platform
        """,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["t-tokelowo@microsoft.com"],
        fail_silently=False,
    )
    print(f"✅ EMAIL SENT SUCCESSFULLY!")
    print(f"📧 Result: {result}")
    print(f"📬 Check your inbox: t-tokelowo@microsoft.com")
    
except Exception as e:
    print(f"❌ EMAIL FAILED: {e}")
    print(f"🔧 Check SendGrid sender verification")
