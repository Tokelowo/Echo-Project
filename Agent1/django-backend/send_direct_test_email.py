import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def send_direct_test_email():
    print("🔧 Sending direct test email using your configured Gmail credentials...")
    print(f"📧 From: {settings.EMAIL_HOST_USER}")
    print(f"🎯 To: t-tokelowo@microsoft.com")
    
    try:
        result = send_mail(
            subject='🔧 DIRECT TEST: Your Email System IS Working!',
            message='''Hi!

This email proves your system CAN send emails successfully.

✅ Gmail credentials: Working
✅ Django email backend: Working  
✅ SMTP connection: Working

The issue is likely in the scheduled report pipeline integration.

Your Reddit integration and email formatting are ready - we just need to fix the pipeline connection.

Best regards,
Your Echo Project System''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['t-tokelowo@microsoft.com'],
            fail_silently=False,
        )
        
        if result == 1:
            print("✅ DIRECT EMAIL SENT SUCCESSFULLY!")
            print("📬 Check your Microsoft inbox - this proves the email system works!")
            return True
        else:
            print("❌ Email sending failed - no emails sent")
            return False
            
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return False

if __name__ == "__main__":
    send_direct_test_email()
