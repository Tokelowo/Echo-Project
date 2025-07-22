import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_direct_email():
    """Send email directly using SMTP without Django"""
    print("🚨 SENDING DIRECT EMAIL TEST...")
    
    # Email configuration (using Gmail SMTP)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_app_email@gmail.com"  # You'll need to configure this
    sender_password = "your_app_password"       # You'll need an app password
    recipient_email = "Temiloluwaokelowo@gmail.com"
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "🚨 URGENT: Daily Email System Test"
    message["From"] = sender_email
    message["To"] = recipient_email
    
    # Create the HTML content
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
          <h1 style="color: #d32f2f;">🚨 EMAIL SYSTEM TEST</h1>
          <p>This is a test email to verify that your daily email system is working.</p>
          
          <div style="background: #f5f5f5; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0;">
            <h3>✅ System Status</h3>
            <p>If you're reading this, the email system is working correctly!</p>
          </div>
          
          <div style="background: #e8f5e8; padding: 15px; border-left: 4px solid #4caf50; margin: 20px 0;">
            <h3>📅 Schedule</h3>
            <p>Daily emails should now be delivered every morning at 9:00 AM.</p>
          </div>
          
          <p><strong>Time sent:</strong> {datetime.now()}</p>
          <p><strong>System:</strong> Direct SMTP Test</p>
          
          <hr style="margin: 30px 0;">
          <p style="color: #666; font-size: 12px;">
            This is an automated test email from your daily email system.
          </p>
        </div>
      </body>
    </html>
    """
    
    # Add HTML part
    html_part = MIMEText(html, "html")
    message.attach(html_part)
    
    try:
        # Send the email
        print("Connecting to SMTP server...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            print("NOTE: You need to configure email credentials in this script.")
            print("For Gmail, you need:")
            print("1. Enable 2-factor authentication")
            print("2. Generate an 'App Password'")
            print("3. Update sender_email and sender_password in this script")
            return False
            
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

if __name__ == "__main__":
    send_direct_email()
