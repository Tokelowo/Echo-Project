import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

try:
    from research_agent.models import EmailSubscription
    
    print("=== CURRENT EMAIL SUBSCRIPTIONS ===")
    subs = EmailSubscription.objects.all()
    
    if subs:
        for sub in subs:
            print(f"✉️  {sub.email}")
            print(f"   Name: {sub.name}")
            print(f"   Active: {sub.is_active}")
            print(f"   Frequency: {sub.frequency}")
            print()
    else:
        print("❌ No subscriptions found")
        
except Exception as e:
    print(f"Error: {e}")
