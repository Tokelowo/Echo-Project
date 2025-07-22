# 🚀 Complete Web App Startup Guide

## **Problem**: Nothing is opening in the browser yet

The terminal commands aren't working through VS Code, so let's use manual startup methods.

## **✅ Solution: Manual Startup (2 Steps)**

### **Step 1: Start React Frontend**

**Option A - Use the batch file I just created:**
1. Open File Explorer
2. Navigate to: `c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React\`
3. Double-click: `start-react-now.bat`
4. A command window will open and start the React server

**Option B - Manual command:**
1. Open Command Prompt or PowerShell
2. Run these commands:
```cmd
cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"
npm run dev
```

### **Step 2: Start Django Backend**

**Option A - Use the batch file I just created:**
1. Open File Explorer  
2. Navigate to: `c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React\`
3. Double-click: `start-django-now.bat`
4. A second command window will open and start Django

**Option B - Manual command:**
1. Open another Command Prompt or PowerShell window
2. Run these commands:
```cmd
cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"
python manage.py runserver 127.0.0.1:8000
```

## **🎯 Expected Results**

### **React Server (Window 1):**
```
VITE v4.5.14  ready in 680 ms
➜  Local:   http://localhost:3000/
➜  Network: http://10.x.x.x:3000/
```

### **Django Server (Window 2):**
```
Django version 4.x.x, using settings 'research_agent.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## **🌐 Open the Web App**

Once both servers are running:

1. **Open your web browser**
2. **Navigate to**: `http://localhost:3000`
3. **You should see**: The competitive intelligence dashboard

## **🎉 What You'll Have Access To**

### **Main Features:**
- ✅ **Dashboard**: Business intelligence overview
- ✅ **Competitive Analysis**: 
  - Internal analytics (existing data)
  - **NEW**: Gartner Reviews tab with market insights
- ✅ **Email System**: Report subscriptions and generation
- ✅ **Accessibility**: Full accessibility controls

### **New Gartner Integration:**
- ✅ Email security vendor comparisons
- ✅ Market insights and trends
- ✅ Customer review analysis
- ✅ Competitive positioning charts

## **🔧 Troubleshooting**

### **If React won't start:**
```cmd
# Check if Node.js is installed
node --version
npm --version

# Install dependencies if needed
cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"
npm install
```

### **If Django won't start:**
```cmd
# Check if Python is installed
python --version

# Install dependencies if needed
cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"
pip install -r requirements.txt
```

### **If port conflicts:**
- React usually runs on port 3000
- Django runs on port 8000
- If ports are busy, the servers will suggest alternatives

## **🚀 Quick Start Commands**

**All-in-one copy-paste for PowerShell:**

```powershell
# Start React (run in first window)
cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Attachments\React"
npm run dev

# Start Django (run in second window)
cd "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend"
python manage.py runserver 127.0.0.1:8000
```

## **📱 Mobile/Network Access**

If you want to access from other devices on your network:
- React: Use the Network URL shown (e.g., `http://10.x.x.x:3000`)
- Django: May need to start with `python manage.py runserver 0.0.0.0:8000`

---

**Ready to experience the full power of your competitive intelligence platform with Gartner integration!** 🎯
