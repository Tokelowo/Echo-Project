# Email Configuration Instructions

## To Enable Real Email Sending:

### 1. Set Environment Variables (Windows PowerShell):
```powershell
$env:EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
$env:EMAIL_HOST_USER = "your_gmail@gmail.com"
$env:EMAIL_HOST_PASSWORD = "your_gmail_app_password"
$env:DEFAULT_FROM_EMAIL = "your_gmail@gmail.com"
```

### 2. Or Create .env file in django-backend folder:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=your_gmail@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=your_gmail@gmail.com
```

### 3. Gmail App Password Setup:
1. Go to Google Account settings
2. Security → 2-Step Verification (must be enabled)
3. App passwords → Generate app password for "Mail"
4. Use that password (not your regular Gmail password)

### 4. Restart Django server after setting credentials

## Current Status:
- ✅ Reddit integration working
- ✅ Email templates with Reddit reviews ready
- ✅ Subscription system configured
- ❌ Email delivery disabled (development mode)

Once you configure the email credentials, your daily emails will be sent automatically!
