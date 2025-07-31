import os
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import datetime

print("=== SENDING PROFESSIONAL HTML EMAIL ===")

# Read the HTML template
try:
    with open('sample_email_with_reddit.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    print("✅ HTML template loaded")
except Exception as e:
    print(f"❌ Error loading HTML template: {e}")
    exit(1)

# Create email
subject = "🛡️ Echo Intelligence - Daily Cybersecurity Report"
from_email = settings.DEFAULT_FROM_EMAIL
to_email = "t-tokelowo@microsoft.com"

# Plain text fallback
text_content = """
Echo Intelligence Daily Report

Your comprehensive cybersecurity intelligence report includes:

• Market trends analysis with real-time data
• Reddit customer experiences and discussions  
• Featured security articles with clickable links
• Microsoft security updates
• Professional metrics and insights
• DOCX attachment with full analysis

This HTML email contains interactive elements and professional formatting.

Best regards,
Echo Intelligence Platform
"""

print(f"From: {from_email}")
print(f"To: {to_email}")
print(f"Subject: {subject}")

try:
    # Create email with HTML and text versions
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to_email]
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    result = email.send()
    
    print(f"✅ PROFESSIONAL HTML EMAIL SENT!")
    print(f"📧 Result: {result}")
    print(f"🎯 Features included:")
    print(f"   • Microsoft Defender branding")
    print(f"   • Professional HTML formatting")
    print(f"   • Reddit reviews with orange styling")
    print(f"   • Clickable article links")
    print(f"   • Metrics cards and charts")
    print(f"   • Executive summary")
    print(f"📬 Check your inbox: {to_email}")
    
except Exception as e:
    print(f"❌ EMAIL FAILED: {e}")
    print(f"🔧 Error details: {str(e)}")
