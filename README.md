# 🛡️ Echo Cybersecurity Intelligence Platform

**A Professional Intelligence Report Generation and Email Delivery System**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![SendGrid](https://img.shields.io/badge/SendGrid-Professional-1A82E2.svg)](https://sendgrid.com)

> **Enterprise-grade cybersecurity intelligence platform that generates professional .docx reports with Microsoft branding and delivers them via automated email subscriptions using SendGrid professional email service.**

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [� Getting Started](#-getting-started)
- [📊 Usage Guide](#-usage-guide)
- [🗂️ API Documentation](#️-api-documentation)
- [🎯 Subscription Management](#-subscription-management)
- [🔒 Security Features](#-security-features)
- [🚀 Deployment](#-deployment)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

### 🎯 **Core Intelligence Capabilities**
- **Real-time Cybersecurity Intelligence** - Live threat data aggregation
- **Microsoft Defender Analysis** - Specialized Office 365 security insights  
- **Professional Report Generation** - Microsoft-branded .docx documents
- **Automated Email Delivery** - SendGrid-powered professional email service
- **Reddit Review Integration** - Real customer feedback analysis
- **Interactive Dashboard** - React-based management interface

### 📊 **Professional Reporting**
- **Microsoft-Branded Documents** - Professional .docx with corporate styling
- **Comprehensive Data Tables** - Structured threat intelligence
- **Executive Summaries** - C-level appropriate briefings
- **Accessibility Compliance** - Times New Roman, proper formatting
- **Real-time Data Analysis** - 100% live intelligence feeds

### 📧 **Enterprise Email System**
- **SendGrid Integration** - Professional email infrastructure
- **Subscription Management** - Automated daily/weekly delivery
- **Personalized Content** - Recipient-specific intelligence
- **Unsubscribe Management** - CAN-SPAM compliant
- **HTML + Plain Text** - Multi-format email support

### 🔒 **Security & Compliance**
- **API Key Authentication** - Secure endpoint access
- **Rate Limiting** - DDoS protection
- **HTTPS Enforcement** - Encrypted communications
- **CSRF Protection** - Cross-site request forgery prevention
- **SQL Injection Prevention** - Parameterized queries

---

## 🏗️ Architecture

```
Echo Cybersecurity Intelligence Platform
├── 🖥️  Frontend (React Dashboard)
│   ├── Material-UI Components
│   ├── Real-time Intelligence Display
│   ├── Subscription Management
│   └── Report Generation Interface
│
├── ⚙️  Backend (Django REST API)
│   ├── 🤖 Intelligence Agents
│   │   ├── Market Trends Agent
│   │   ├── Comprehensive Research Agent
│   │   └── Formatting Agent (Microsoft .docx)
│   │
│   ├── 📧 Email Service (SendGrid)
│   │   ├── Professional Sender Identity
│   │   ├── HTML Email Templates
│   │   ├── Attachment Management
│   │   └── Subscription Automation
│   │
│   ├── 🗄️ Database (SQLite)
│   │   ├── Subscription Management
│   │   ├── Report History
│   │   ├── User Preferences
│   │   └── Intelligence Cache
│   │
│   └── 🔒 Security Layer
│       ├── API Authentication
│       ├── Rate Limiting
│       ├── CORS Management
│       └── Input Validation
│
└── 🌐 External Integrations
    ├── SendGrid Email API
    ├── OpenAI Intelligence Processing
    ├── Reddit Customer Reviews
    └── Real-time Threat Feeds
```

---

## � Getting Started

For complete setup instructions, see **[TEAM_SETUP.md](TEAM_SETUP.md)** - our step-by-step guide for getting the Echo Intelligence Platform running on your machine.

**Quick Overview:**
1. Clone the repository: `git clone https://github.com/Tokelowo/Echo-Project.git`
2. Follow the detailed setup guide in [TEAM_SETUP.md](TEAM_SETUP.md)
3. Access the dashboard at http://localhost:3000

### 📋 **System Requirements**
- **Python 3.8+** and **Node.js 16+**
- **Git** for version control
- **SendGrid API Key** for email delivery
- **OpenAI API Key** for intelligence processing

---

## 📊 Usage Guide

### 🖥️ **Dashboard Interface**

**Accessing the Dashboard:**
1. Start both backend and frontend servers
2. Navigate to http://localhost:3000
3. Main dashboard displays cybersecurity intelligence

**Dashboard Features:**
- **Latest Intelligence Reports** - Real-time threat data
- **Subscription Management** - Email delivery controls
- **Report Generation** - On-demand intelligence reports
- **Customer Reviews** - Reddit integration showing real feedback

### 📧 **Email Subscription Management**

**Subscribe to Intelligence Reports:**

```python
# Using Python requests
import requests

subscription_data = {
    "user_email": "user@company.com",
    "user_name": "John Doe",
    "agent_type": "comprehensive_research",  # or "market_trends_agent"
    "frequency": "daily",  # or "weekly"
    "preferred_time": "09:00",
    "time_zone": "PST"
}

response = requests.post(
    "http://localhost:8000/api/subscribe/",
    json=subscription_data
)
```

**Via Dashboard:**
1. Click **Subscribe to Reports**
2. Enter email and preferences
3. Choose agent type and frequency
4. Confirm subscription

### 🤖 **Intelligence Agents**

**Available Agents:**

1. **Market Trends Agent**
   - Focus: Market analysis and trends
   - Update Frequency: Daily
   - Content: Strategic business intelligence

2. **Comprehensive Research Agent**
   - Focus: Deep cybersecurity analysis
   - Update Frequency: Daily
   - Content: Technical threat intelligence

**Manual Report Generation:**
```bash
# Generate comprehensive report
python manage.py shell
>>> from research_agent.cybersecurity_news_service_new import CybersecurityNewsService
>>> service = CybersecurityNewsService()
>>> report = service.generate_comprehensive_report()
>>> print(report)
```

### 📋 **Report Formats**

**Generated Reports Include:**
- **Executive Summary** - C-level briefing
- **Threat Analysis** - Technical details
- **Customer Reviews** - Real user feedback
- **Recommendations** - Actionable insights
- **Charts and Tables** - Visual data representation

**Output Formats:**
- **.docx** - Professional Microsoft Word document
- **HTML Email** - Rich formatting with embedded charts
- **Plain Text** - Email client compatibility

---

## 🗂️ API Documentation

### 🔗 **Base URL**
```
Local Development: http://localhost:8000/api/
Production: https://your-domain.com/api/
```

### 🔐 **Authentication**

**API Key Authentication:**
```bash
# Include in headers
X-API-Key: your-api-secret-key

# Example curl request
curl -H "X-API-Key: your-api-secret-key" \
     http://localhost:8000/api/intelligence-reports/
```

### 📡 **API Endpoints**

#### **Intelligence Reports**

**Get Latest Report:**
```http
GET /api/intelligence-reports/latest/
```

**Generate New Report:**
```http
POST /api/intelligence-reports/generate/
Content-Type: application/json

{
    "agent_type": "comprehensive_research",
    "include_reviews": true,
    "format": "both"
}
```

#### **Subscription Management**

**Create Subscription:**
```http
POST /api/subscribe/
Content-Type: application/json

{
    "user_email": "user@company.com",
    "user_name": "John Doe",
    "agent_type": "comprehensive_research",
    "frequency": "daily",
    "preferred_time": "09:00",
    "time_zone": "PST"
}
```

**Update Subscription:**
```http
PUT /api/subscriptions/{id}/
Content-Type: application/json

{
    "frequency": "weekly",
    "preferred_time": "08:00"
}
```

**Unsubscribe:**
```http
DELETE /api/subscriptions/{id}/
```

#### **Email Delivery**

**Send Test Email:**
```http
POST /api/email/test/
Content-Type: application/json

{
    "recipient_email": "test@company.com",
    "recipient_name": "Test User",
    "report_type": "preview"
}
```

**Check Email Status:**
```http
GET /api/email/status/{delivery_id}/
```

#### **Customer Reviews**

**Get Reviews:**
```http
GET /api/customer-reviews/
?product=Microsoft+Defender+for+Office+365
&limit=5
```

### 📊 **Response Formats**

**Success Response:**
```json
{
    "status": "success",
    "message": "Report generated successfully",
    "data": {
        "report_id": "report_20250729_1230",
        "title": "Cybersecurity Intelligence Report",
        "generated_at": "2025-07-29T12:30:00Z",
        "docx_filename": "MDO_Report_Intelligence_20250729_1230.docx"
    }
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Invalid API key",
    "error_code": "AUTH_001",
    "details": {
        "required": ["X-API-Key header"]
    }
}
```

---

## 🎯 Subscription Management

### 📋 **Subscription Lifecycle**

**1. Subscription Creation:**
- User provides email and preferences
- System creates database record
- Confirmation email sent (optional)
- Scheduled delivery begins

**2. Report Generation:**
- Automated daily/weekly triggers
- AI agents gather intelligence
- Professional .docx reports created
- Email delivery via SendGrid

**3. Delivery Management:**
- HTML + Plain text emails
- Professional Microsoft branding
- Unsubscribe links included
- Delivery status tracking

### 🔧 **Administrative Tools**

**Check Subscription Status:**
```python
# Run from django-backend directory
python check_subscription_status.py
```

**Manual Email Delivery:**
```python
# Send test email
python send_test_email_now.py

# Send to all subscribers
python send_daily_emails_improved.bat
```

**Database Management:**
```python
# Django shell access
python manage.py shell

# Check all subscriptions
>>> from research_agent.models import ReportSubscription
>>> subscriptions = ReportSubscription.objects.all()
>>> for sub in subscriptions:
...     print(f"{sub.user_email} - {sub.agent_type} - Active: {sub.is_active}")
```

### 📊 **Subscription Analytics**

**Delivery Statistics:**
- Total emails sent
- Delivery success rate
- Bounce/failure tracking
- Subscriber engagement metrics

**Performance Monitoring:**
- Report generation time
- Email delivery speed
- System resource usage
- Error tracking and alerts

---

## 🔒 Security Features

### 🛡️ **Built-in Security**

**API Protection:**
- API key authentication
- Rate limiting (120/min, 2000/hour)
- Request size limits (10MB max)
- Input validation and sanitization

**Web Security:**
- HTTPS enforcement
- CSRF protection
- XSS prevention
- SQL injection prevention
- Clickjacking protection

**Email Security:**
- SendGrid professional infrastructure
- CAN-SPAM compliance
- Unsubscribe management
- Sender authentication

### 🔑 **Authentication Setup**

**API Key Generation:**
```python
import secrets
api_key = secrets.token_urlsafe(32)
print(f"Your API Key: {api_key}")
```

**Secure Headers:**
```python
# Add to middleware
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
```

### 🚨 **Security Monitoring**

**Rate Limiting:**
- Automatic blocking of excessive requests
- IP-based throttling
- User-specific limits
- Whitelist for trusted IPs

**Logging and Alerts:**
- Failed authentication attempts
- Suspicious activity patterns
- Email delivery failures
- System performance issues

---

## 🚀 Deployment

### 🌐 **Production Deployment**

**Environment Preparation:**
1. **Linux Server** (Ubuntu/CentOS recommended)
2. **Python 3.8+** and **pip**
3. **Nginx** web server
4. **Supervisor** for process management
5. **SSL Certificate** (Let's Encrypt recommended)

**Deployment Steps:**

**1. Server Setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv nginx supervisor git -y

# Clone repository
git clone https://github.com/Tokelowo/Echo-Project.git
cd Echo-Project
```

**2. Backend Deployment:**
```bash
cd Agent1/django-backend

# Create production virtual environment
python3 -m venv prod_env
source prod_env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary  # For production server

# Set production environment variables
cp .env.example .env.production
# Edit .env.production with production settings

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

**3. Frontend Build:**
```bash
cd ../../React

# Install dependencies
npm install

# Build for production
npm run build

# Copy build files to web server
sudo cp -r dist/* /var/www/html/echo-intelligence/
```

**4. Nginx Configuration:**
```nginx
# /etc/nginx/sites-available/echo-intelligence
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/ssl/certificate.crt;
    ssl_certificate_key /path/to/ssl/private.key;

    # Frontend static files
    location / {
        root /var/www/html/echo-intelligence;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django admin
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**5. Supervisor Configuration:**
```ini
# /etc/supervisor/conf.d/echo-intelligence.conf
[program:echo-django]
command=/path/to/Echo-Project/Agent1/django-backend/prod_env/bin/gunicorn backend.wsgi:application --bind 127.0.0.1:8000 --workers 3
directory=/path/to/Echo-Project/Agent1/django-backend
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/echo-intelligence/django.log
```

**6. Start Services:**
```bash
# Enable and start services
sudo systemctl enable nginx supervisor
sudo systemctl start nginx supervisor

# Reload configurations
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start echo-django

# Check status
sudo supervisorctl status
```

### 🔄 **Automated Deployment**

**GitHub Actions CI/CD:**
```yaml
# .github/workflows/deploy.yml
name: Deploy Echo Intelligence

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.KEY }}
        script: |
          cd /path/to/Echo-Project
          git pull origin main
          # Add deployment commands here
```

### 📈 **Production Monitoring**

**Health Checks:**
```bash
# Create monitoring script
cat > health-check.sh << 'EOF'
#!/bin/bash
curl -f http://localhost:8000/api/health/ || exit 1
curl -f http://localhost:3000/ || exit 1
echo "All services healthy"
EOF

chmod +x health-check.sh
```

**Log Monitoring:**
```bash
# Monitor Django logs
tail -f /var/log/echo-intelligence/django.log

# Monitor Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## 🛠️ Troubleshooting

### 🚨 **Common Issues**

### **1. Email Delivery Failures**

**Problem:** Emails not sending
```bash
# Check SendGrid configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@domain.com', ['to@domain.com'])
```

**Solutions:**
- Verify SendGrid API key
- Check sender authentication
- Confirm email quotas not exceeded
- Review .env configuration

### **2. Database Connection Issues**

**Problem:** Django database errors
```bash
# Check database status
python manage.py dbshell
# Run: .tables to see if tables exist

# Reset database if needed
rm db.sqlite3
python manage.py migrate
```

**Solutions:**
- Ensure SQLite permissions
- Run migrations: `python manage.py migrate`
- Check database file location
- Verify Django settings

### **3. Frontend Build Errors**

**Problem:** React build failures
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

**Solutions:**
- Update Node.js version (16+)
- Clear npm cache: `npm cache clean --force`
- Check for dependency conflicts
- Verify build scripts in package.json

### **4. API Authentication Issues**

**Problem:** 401/403 API errors
```bash
# Test API endpoint
curl -H "X-API-Key: your-key-here" \
     http://localhost:8000/api/intelligence-reports/
```

**Solutions:**
- Verify API key in .env file
- Check middleware configuration
- Confirm headers in requests
- Review CORS settings

### **5. Port Conflicts**

**Problem:** "Port already in use" errors

**Find processes using ports:**
```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# macOS/Linux
lsof -i :8000
lsof -i :3000
```

**Solutions:**
- Kill existing processes
- Use different ports
- Check for running containers
- Restart system if needed

### 📋 **Debug Mode Setup**

**Enable Detailed Logging:**
```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'research_agent': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

**Check System Status:**
```python
# Create system_check.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from research_agent.enhanced_email_service import EnhancedEmailService

# Test email service
service = EnhancedEmailService()
result = service.validate_email_setup()
print("Email Setup:", result)

# Test database
from research_agent.models import ReportSubscription
print("Subscriptions:", ReportSubscription.objects.count())
```

### 🔧 **Performance Optimization**

**Database Optimization:**
```python
# Add database indexes
from django.db import models

class ReportSubscription(models.Model):
    user_email = models.EmailField(db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    # ... other fields
```

**Caching Setup:**
```python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
```

---

## 🤝 Contributing

### 🛠️ **Development Workflow**

**1. Fork the Repository**
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/your-username/Echo-Project.git
cd Echo-Project
```

**2. Create Feature Branch**
```bash
git checkout -b feature/new-intelligence-source
```

**3. Development Environment**
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest django-debug-toolbar

# Run tests
python manage.py test

# Start development servers (see TEAM_SETUP.md for details)
python manage.py runserver &
cd React && npm run dev
```

**4. Code Quality Standards**
```bash
# Python code formatting
pip install black flake8
black . --exclude=venv
flake8 . --exclude=venv

# JavaScript/React formatting
npm install --save-dev prettier
npx prettier --write src/
```

**5. Testing Requirements**
```python
# Write tests for new features
# tests/test_email_service.py
from django.test import TestCase
from research_agent.enhanced_email_service import EnhancedEmailService

class EmailServiceTests(TestCase):
    def test_email_validation(self):
        service = EnhancedEmailService()
        result = service.validate_email_setup()
        self.assertTrue(result['overall_status'])
```

**6. Submit Pull Request**
```bash
git add .
git commit -m "feat: Add new intelligence source integration"
git push origin feature/new-intelligence-source
# Create PR on GitHub
```

### 📋 **Contribution Guidelines**

**Code Standards:**
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation for API changes

**Commit Message Format:**
```
feat: Add customer review sentiment analysis
fix: Resolve email delivery timeout issue
docs: Update API documentation for subscriptions
style: Format code according to black standards
test: Add unit tests for formatting agent
```

**Pull Request Template:**
- Clear description of changes
- Screenshots for UI changes
- Test coverage information
- Breaking change notifications
- Documentation updates included

### 🎯 **Areas for Contribution**

**High Priority:**
- Additional intelligence sources
- Enhanced email templates
- Mobile-responsive dashboard
- Advanced analytics dashboard
- Multi-language support

**Medium Priority:**
- Slack/Teams integrations
- PDF report generation
- Advanced filtering options
- User authentication system
- Webhook integrations

**Nice to Have:**
- Dark mode theme
- Email scheduling UI
- Report customization options
- Advanced search features
- Performance optimizations

---

## 📞 **Support & Contact**

### 📧 **Getting Help**

**GitHub Issues:**
- Bug reports: Use bug report template
- Feature requests: Use feature request template
- Questions: Use discussion board

**Documentation:**
- API Documentation: `/docs/api/`
- User Guide: `/docs/user-guide/`
- Developer Guide: `/docs/development/`

**Community:**
- Discord Server: [Join our community](https://discord.gg/echo-intelligence)
- Stack Overflow: Tag questions with `echo-intelligence`

### 🔄 **Version History**

**Current Version: 2.1.0**
- ✅ SendGrid professional email integration
- ✅ Microsoft-branded .docx reports
- ✅ React dashboard with Material-UI
- ✅ Real-time customer review integration
- ✅ Automated subscription management
- ✅ Professional sender identity

**Roadmap v2.2.0:**
- 🔄 Multi-language email templates
- 🔄 Advanced analytics dashboard
- 🔄 Slack/Teams integration
- 🔄 Mobile app companion

---

## 📄 License

**MIT License**

```
MIT License

Copyright (c) 2025 Echo Cybersecurity Intelligence Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 **Acknowledgments**

**Third-Party Services:**
- **SendGrid** - Professional email delivery infrastructure
- **OpenAI** - AI-powered intelligence processing
- **Material-UI** - React component library
- **Django REST Framework** - API development framework

**Open Source Libraries:**
- **React** - Frontend framework by Facebook
- **Django** - Python web framework
- **Vite** - Frontend build tool
- **python-docx** - Microsoft Word document generation

**Community:**
- Contributors and beta testers
- Cybersecurity community feedback
- Open source maintainers

---

**🚀 Ready to deploy professional cybersecurity intelligence? Get started now!**

```bash
git clone https://github.com/Tokelowo/Echo-Project.git
cd Echo-Project
# Follow TEAM_SETUP.md for complete setup instructions
```

**New to the project?**
- 📋 **Quick Setup**: Follow [TEAM_SETUP.md](TEAM_SETUP.md) for step-by-step instructions
- 📖 **Full Documentation**: This README for comprehensive platform details
- 🎯 **API Reference**: See the API Documentation section above

**Questions? Issues? Contributions?**
- 📧 Create an issue on GitHub
- 💬 Join our Discord community  
- 🌟 Star the repository if it helps you!

---

*Last updated: July 29, 2025 | Version 2.1.0*
