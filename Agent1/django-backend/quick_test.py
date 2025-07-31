import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.mail import send_mail

try:
    result = send_mail(
        'Test Email from Echo Intelligence',
        'Testing the email system with current configuration.',
        'Temiloluwaokelowo@gmail.com',
        ['t-tokelowo@microsoft.com'],
        fail_silently=False,
    )
    print(f"SUCCESS: Email sent! Result: {result}")
except Exception as e:
    print(f"ERROR: {e}")
