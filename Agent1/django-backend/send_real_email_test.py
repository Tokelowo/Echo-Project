import os
import django
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Test real email sending
def send_test_email():
    print("🔧 Testing real email delivery...")
    
    # Gmail SMTP configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # You'll need to provide your email credentials
    sender_email = "your_email@gmail.com"  # Replace with your Gmail
    sender_password = "your_app_password"   # Replace with Gmail App Password
    
    recipient_email = "t-tokelowo@microsoft.com"
    
    # Create email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "🔧 TEST: Reddit Integration Email System"
    
    # Email body
    body = """
    <html>
    <body>
        <h2>🧪 Email System Test - Reddit Integration Working!</h2>
        <p>Hi there!</p>
        <p>This is a test email to confirm the Reddit integration system is working.</p>
        
        <div style="background-color: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #ff4500;">
            <h3 style="color: #ff4500;">📧 System Status:</h3>
            <ul>
                <li>✅ Django backend running</li>
                <li>✅ React frontend running</li>
                <li>✅ Reddit integration implemented</li>
                <li>✅ Email formatting with orange Reddit theme</li>
                <li>✅ Subscription system active</li>
            </ul>
        </div>
        
        <p><strong>Next Steps:</strong></p>
        <p>1. Configure email credentials properly</p>
        <p>2. Your daily emails will be sent automatically at 9:00 AM UTC</p>
        <p>3. Each email will include Reddit reviews with clickable links</p>
        
        <p>Best regards,<br>Your Echo Project System</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # Connect to Gmail SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ TEST EMAIL SENT SUCCESSFULLY!")
        print(f"📧 Sent to: {recipient_email}")
        
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        print("📝 Note: You need to configure Gmail credentials for real email sending")
        print("🔧 For now, emails are being logged to console only")

if __name__ == "__main__":
    send_test_email()
