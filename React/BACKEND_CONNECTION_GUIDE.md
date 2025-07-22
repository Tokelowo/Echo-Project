# Backend Connection Troubleshooting Guide

## 🔧 Quick Fix - Start Django Backend

The React frontend is trying to connect to the Django backend at `http://127.0.0.1:8000` but the server isn't running.

### **Method 1: PowerShell Script (Recommended)**
```powershell
# Navigate to React directory and run the PowerShell script
cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"
.\start-django.ps1
```

### **Method 2: Manual Start**
```powershell
# Navigate to Django backend directory
cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"

# Start Django server
python manage.py runserver 127.0.0.1:8000
```

### **Method 3: Use Existing Batch File**
```cmd
# Run the existing batch file
"c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\start_both_servers.bat"
```

## 🎯 Expected Results

Once the Django server starts successfully, you should see:
```
✅ Django version 4.2.x, using settings 'research_agent.settings'
✅ Starting development server at http://127.0.0.1:8000/
✅ Quit the server with CTRL-BREAK.
```

## 🔍 Verify Backend is Running

Test the API endpoints:
- **Dashboard Data**: http://127.0.0.1:8000/research-agent/overview/
- **Competitive Metrics**: http://127.0.0.1:8000/research-agent/competitive-metrics/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🚀 Complete Setup Instructions

### **For Full Application (Backend + Frontend):**

1. **Start Django Backend**:
   ```powershell
   cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"
   python manage.py runserver 127.0.0.1:8000
   ```

2. **Start React Frontend** (already running):
   ```powershell
   cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"
   npm run dev
   ```

3. **Open Browser**:
   - Frontend: http://localhost:3000
   - Backend API: http://127.0.0.1:8000

## ⚡ Features Available Once Connected

### **Dashboard Features:**
- ✅ Email system status and subscriptions
- ✅ Competitive intelligence metrics
- ✅ Market trends analysis
- ✅ Real-time data updates

### **New Gartner Integration:**
- ✅ Vendor comparison tables
- ✅ Market insights dashboard
- ✅ Customer review analysis
- ✅ Competitive positioning charts

### **Email System:**
- ✅ Daily email reports (9:00 AM scheduled)
- ✅ One-time professional reports
- ✅ Subscription management
- ✅ Microsoft-branded email templates

## 🐛 Common Issues & Solutions

### **Issue**: Django server won't start
**Solution**: Check if Python dependencies are installed:
```powershell
cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"
pip install -r requirements.txt
```

### **Issue**: Port 8000 already in use
**Solution**: Kill existing processes or use different port:
```powershell
# Kill processes on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Or start on different port
python manage.py runserver 127.0.0.1:8001
```

### **Issue**: CORS errors in browser
**Solution**: Django CORS is configured for React development server. Ensure both servers are running on correct ports.

## 🎉 Success Indicators

When everything is working correctly:
- ✅ Django server running on http://127.0.0.1:8000
- ✅ React frontend on http://localhost:3000  
- ✅ No "Failed to fetch" errors in browser console
- ✅ Dashboard loads with real data
- ✅ Gartner Reviews tab shows market data
- ✅ Email subscription features work

The application combines the Django backend's competitive intelligence with the React frontend's modern UI, including the new Gartner Peer Insights integration for comprehensive market analysis!
