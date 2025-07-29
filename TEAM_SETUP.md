# 🚀 Echo Intelligence - Team Setup Guide

**Quick setup guide for team members to get the Echo Cybersecurity Intelligence Platform running locally.**

---

## 📋 What You Need Before Starting

### 🖥️ **Required Software**
- **Python 3.8+** ([Download here](https://python.org/downloads/))
- **Node.js 16+** ([Download here](https://nodejs.org/))
- **Git** ([Download here](https://git-scm.com/downloads))
- **Code Editor** (VS Code recommended)

### 🔑 **Required API Keys** (Ask team lead for these)
- **SendGrid API Key** - For email delivery
- **OpenAI API Key** - For AI report generation

---

## 🚀 Quick Setup (5 Minutes)

### **Step 1: Get the Code**
```bash
# Clone from GitHub
git clone https://github.com/Tokelowo/Echo-Project.git
cd Echo-Project
```

### **Step 2: Backend Setup**
```bash
# Go to backend folder
cd Agent1/django-backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# Activate it (Mac/Linux)
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### **Step 3: Configure Environment**
```bash
# Create environment file
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux

# Edit .env file with these settings:
```

**Put this in your `.env` file:**
```
SECRET_KEY=your-secret-key-here-make-it-long-and-random
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Get these from team lead)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.your_sendgrid_api_key_here
DEFAULT_FROM_EMAIL=your-team-email@domain.com

# AI Services (Get from team lead)
OPENAI_API_KEY=your_openai_api_key_here

# Security (Generate random strings)
API_SECRET_KEY=some-random-string-here
```

### **Step 4: Setup Database**
```bash
# Still in Agent1/django-backend folder
python manage.py migrate
python manage.py createsuperuser  # Optional: create admin account
```

### **Step 5: Frontend Setup**
```bash
# Open NEW terminal, go to React folder
cd React

# Install packages
npm install
```

### **Step 6: Start Both Servers**
```bash
# Terminal 1 - Backend (in Agent1/django-backend)
python manage.py runserver

# Terminal 2 - Frontend (in React folder)  
npm run dev
```

### **Step 7: Access the App**
- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

---

## 🔧 Generate Required Keys

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Generate API_SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🛠️ Common Issues & Fixes

### **❌ "Port already in use"**
```bash
# Kill processes on ports
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### **❌ "Module not found" errors**
```bash
# Make sure virtual environment is activated
# You should see (venv) in your terminal prompt
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall if needed
pip install -r requirements.txt
```

### **❌ Database errors**
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```

### **❌ npm install fails**
```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## 📁 Project Structure (What's What)

```
Echo-Project/
├── Agent1/django-backend/    # Python backend (API, database, email)
│   ├── research_agent/       # Main app logic
│   ├── requirements.txt      # Python packages
│   ├── manage.py            # Django commands
│   └── .env                 # Your config file
│
├── React/                   # Frontend dashboard
│   ├── src/                 # React components
│   ├── package.json         # Node packages
│   └── vite.config.js       # Build config
│
└── README.md               # Detailed documentation
```

---

## 🚀 Daily Development Workflow

### **Starting Work:**
```bash
# Terminal 1 - Backend
cd Agent1/django-backend
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
python manage.py runserver

# Terminal 2 - Frontend  
cd React
npm run dev
```

### **Making Changes:**
1. **Backend changes**: Edit files in `Agent1/django-backend/research_agent/`
2. **Frontend changes**: Edit files in `React/src/`
3. **Database changes**: Run `python manage.py makemigrations` then `python manage.py migrate`

### **Pushing Changes:**
```bash
git add .
git commit -m "your change description"
git push origin main
```

### **Getting Latest Changes:**
```bash
git pull origin main
# If backend requirements changed:
pip install -r requirements.txt
# If frontend packages changed:
npm install
```

---


### **Test Backend:**
Visit: http://localhost:8000/admin
- Should see Django admin login

### **Test Frontend:**
Visit: http://localhost:3000
- Should see the Intelligence Dashboard

### **Test Email Service:**
```bash
# In django-backend folder
python send_test_email_now.py
```

### **Check Database:**
```bash
python manage.py shell
>>> from research_agent.models import ReportSubscription
>>> print(ReportSubscription.objects.count())
```

---


### **Quick Fixes:**
1. **Restart both servers** - Solves 80% of issues
2. **Check virtual environment is activated** - Should see `(venv)` in terminal
3. **Update packages** - `pip install -r requirements.txt` and `npm install`
4. **Reset database** - Delete `db.sqlite3` and run `python manage.py migrate`

### **Still Stuck?**
- 💬 Ask in team chat
- 📧 Create GitHub issue
- 🔍 Check the main README.md for detailed docs
- 📱 Message team lead with error screenshots

---

## 🎯 What Each Service Does

- **Django Backend (Port 8000)**: 
  - Handles API requests
  - Generates intelligence reports
  - Manages email subscriptions
  - Stores data in SQLite database

- **React Frontend (Port 3000)**:
  - Shows the dashboard interface
  - Lets users subscribe to reports
  - Displays intelligence data
  - Manages user interactions

- **SendGrid Email**:
  - Sends professional intelligence reports
  - Handles subscription emails
  - Provides delivery tracking

---

**🎉 You're ready to contribute to Echo Intelligence!**

*Questions? Ask the team lead or check the detailed README.md for more info.*
