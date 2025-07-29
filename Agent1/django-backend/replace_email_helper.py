#!/usr/bin/env python3
"""
Email Replacement Helper Script
This script helps you replace your Microsoft email with a professional one
"""
import os
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def replace_email_configuration():
    """Guide user through email replacement process"""
    
    print("🔄 EMAIL REPLACEMENT PROCESS")
    print("=" * 50)
    
    print("\n📧 CURRENT EMAIL CONFIGURATION:")
    print("- Current sender: t-tokelowo@microsoft.com")
    print("- Display name: Echo Cybersecurity Intelligence")
    print("- Email service: SendGrid")
    
    print("\n🎯 TO COMPLETELY REPLACE YOUR EMAIL:")
    print("\n1. CREATE NEW PROFESSIONAL EMAIL:")
    print("   - Go to gmail.com")
    print("   - Create: echo.cybersecurity.reports@gmail.com")
    print("   - Enable 2FA and generate App Password")
    
    print("\n2. UPDATE SENDGRID:")
    print("   - Go to SendGrid → Sender Authentication")
    print("   - Create new sender with professional email")
    print("   - Verify the new email address")
    print("   - Get new API key if needed")
    
    print("\n3. UPDATE YOUR .ENV FILE:")
    print("   Replace in .env file:")
    print("   OLD: DEFAULT_FROM_EMAIL=Echo Cybersecurity Intelligence <t-tokelowo@microsoft.com>")
    print("   NEW: DEFAULT_FROM_EMAIL=Echo Cybersecurity Intelligence <echo.cybersecurity.reports@gmail.com>")
    
    print("\n4. UPDATE EMAIL SERVICE CODE:")
    print("   Replace in enhanced_email_service.py:")
    print("   OLD: professional_from_email = \"Echo Cybersecurity Intelligence <t-tokelowo@microsoft.com>\"")
    print("   NEW: professional_from_email = \"Echo Cybersecurity Intelligence <echo.cybersecurity.reports@gmail.com>\"")
    
    print("\n5. TEST THE NEW CONFIGURATION:")
    print("   Run: python test_sendgrid_email.py")
    
    print("\n6. YOUR SUBSCRIPTIONS:")
    print("   ✅ Your existing subscriptions will continue working")
    print("   ✅ Only the sender email changes, not recipient emails")
    
    print("\n📝 RECOMMENDED PROFESSIONAL EMAIL NAMES:")
    print("   - echo.cybersecurity.reports@gmail.com")
    print("   - cybersec.intelligence@gmail.com")
    print("   - echo.threat.intel@gmail.com")
    print("   - security.reports.echo@gmail.com")
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("   - Your subscriptions (t-tokelowo@microsoft.com) stay the same")
    print("   - Only the 'FROM' sender changes")
    print("   - You'll still receive reports at your Microsoft email")
    print("   - Recipients will see the professional sender")
    
    new_email = input("\n✏️  Enter your new professional email (or 'skip' to exit): ")
    
    if new_email.lower() != 'skip' and '@' in new_email:
        print(f"\n🎯 NEXT STEPS FOR: {new_email}")
        print("1. Create this Gmail account")
        print("2. Set up SendGrid sender authentication")
        print("3. Come back and I'll update your configuration files")
        print(f"4. Test with: Echo Cybersecurity Intelligence <{new_email}>")
    
    print("\n💡 TIP: Keep your Microsoft email for receiving reports!")
    print("Only the sender identity changes, not where you receive emails.")

if __name__ == "__main__":
    replace_email_configuration()
