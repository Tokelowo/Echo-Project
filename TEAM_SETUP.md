# 🚀 Echo Intelligence - Team Setup Guide for Beginners

**A complete, step-by-step guide for team members with little to no technical experience to get the Echo Cybersecurity Intelligence Platform running on their computer.**

*Don't worry if you're not technical - this guide explains everything in simple terms!*

---

## 📋 What You Need Before Starting

Think of this like gathering ingredients before cooking. We need to install some programs on your computer first.

### 🖥️ **Required Software (Programs You Need to Install)**

#### 1. **Python 3.8+** - The "brain" that runs our backend
- **What it is**: A programming language that powers our email system and data processing
- **Download**: Go to [https://python.org/downloads/](https://python.org/downloads/)
- **Installation tip**: 
  - ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
  - ✅ Choose "Install for all users" if asked
  - ✅ Click "Disable path length limit" at the end if prompted

#### 2. **Node.js 16+** - Powers our website interface
- **What it is**: JavaScript runtime that makes our dashboard work
- **Download**: Go to [https://nodejs.org/](https://nodejs.org/) 
- **Which version**: Download the "LTS" (Long Term Support) version - it's the stable one
- **Installation tip**: Use all default settings, just keep clicking "Next"

#### 3. **Git** - Version control (keeps track of code changes)
- **What it is**: Like "Google Docs version history" but for code
- **Download**: Go to [https://git-scm.com/downloads](https://git-scm.com/downloads)
- **Installation tip**: 
  - Use default settings for most options
  - When asked about "default editor", choose "Visual Studio Code" if you have it

#### 4. **Visual Studio Code** (Recommended code editor)
- **What it is**: A text editor designed for code (like Microsoft Word but for programmers)
- **Download**: Go to [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **Why we recommend it**: It has helpful features and good integration with our project

### 🔑 **Required API Keys** 

These are like passwords that let our system talk to external services. You can get these yourself or ask your team lead:

#### **SendGrid API Key** - Lets us send professional emails
- **What it is**: Service that sends our intelligence reports via email
- **How to get it**:
  1. Go to [SendGrid.com](https://sendgrid.com/) and create a free account
  2. Complete email verification and account setup
  3. Navigate to **Settings** → **API Keys** → **Create API Key**
  4. Choose **Full Access** permissions
  5. Copy the API key (starts with `SG.`)
- **Free tier**: 100 emails/day (perfect for development)
- **Alternative**: Ask team lead for existing key

#### **OpenAI API Key** - Powers our AI report generation
- **What it is**: AI service that generates our cybersecurity intelligence reports
- **How to get it**:
  
  **Option 1: Azure AI Foundry (Recommended for Microsoft users)**
  1. Go to [Azure AI Foundry](https://ai.azure.com/)
  2. Sign in with your Microsoft account
  3. Create a new project or use existing one
  4. Go to **Settings** → **Connections** → **Add Connection**
  5. Select **Azure OpenAI** and deploy a model (like GPT-4)
  6. Copy the **Endpoint URL** and **API Key**
  
  **Option 2: OpenAI Direct**
  1. Go to [OpenAI Platform](https://platform.openai.com/)
  2. Create account and verify phone number
  3. Go to **API Keys** → **Create new secret key**
  4. Copy the key (starts with `sk-`)
  
- **Cost**: Pay-per-use (usually $5-20/month for development)
- **Alternative**: Ask team lead for existing key

#### **Reddit API Keys** (Optional - for customer reviews)
- **What it is**: Fetches real customer discussions about cybersecurity products
- **How to get it**:
  1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
  2. Create a **script** application
  3. Copy **Client ID** and **Client Secret**
- **Free**: Yes, with reasonable rate limits
- **Alternative**: System works without it (uses sample data)

---

## 🚀 Step-by-Step Setup (Follow Each Step Carefully)

### **Step 1: Get the Code from GitHub**

**What we're doing**: Downloading our project code to your computer

1. **Open Command Prompt** (Windows) or **Terminal** (Mac):
   - **Windows**: Press `Windows key + R`, type `cmd`, press Enter
   - **Mac**: Press `Cmd + Space`, type `terminal`, press Enter

2. **Navigate to where you want the project**:
   ```bash
   # Go to your Documents folder (safe place to put projects)
   cd Documents
   ```

3. **Download the project**:
   ```bash
   # This downloads our entire project to your computer
   git clone https://github.com/Tokelowo/Echo-Project.git
   
   # Enter the project folder
   cd Echo-Project
   ```

**What just happened**: You now have a copy of our project on your computer in your Documents folder!

### **Step 2: Set Up the Backend (The "Server Brain")**

**What we're doing**: Setting up the Python part that handles data and emails

1. **Navigate to the backend folder**:
   ```bash
   # Move into the backend directory
   cd Agent1/django-backend
   ```

2. **Create a virtual environment** (like a separate workspace for our project):
   ```bash
   # Create a virtual environment (think of it as a clean workspace)
   python -m venv venv
   ```
   
   **What this does**: Creates a folder called `venv` that keeps our project's Python packages separate from your computer's main Python installation.

3. **Activate the virtual environment**:
   
   **For Windows**:
   ```bash
   venv\Scripts\activate
   ```
   
   **For Mac/Linux**:
   ```bash
   source venv/bin/activate
   ```
   
   **Success indicator**: You should see `(venv)` at the beginning of your command line. This means you're now working in the project's environment.

4. **Install required Python packages**:
   ```bash
   # This installs all the Python libraries our project needs
   pip install -r requirements.txt
   ```
   
   **What this does**: Reads a list of required software components and installs them. This might take a few minutes.

### **Step 3: Configure Your Environment File**

**What we're doing**: Creating a settings file that tells our system how to work

1. **Create your settings file**:
   
   **For Windows**:
   ```bash
   copy .env.example .env
   ```
   
   **For Mac/Linux**:
   ```bash
   cp .env.example .env
   ```

2. **Edit the settings file**:
   - **Option A**: Use VS Code: `code .env`
   - **Option B**: Use any text editor (Notepad, TextEdit, etc.)
   - **Option C**: Right-click the `.env` file and choose "Open with" → "Notepad"

3. **Fill in your settings** (replace the placeholder text with the API keys you obtained above):

```properties
# Django Configuration (the web framework we use)
SECRET_KEY=your-secret-key-here-make-it-long-and-random-123456789abcdef
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (how we send emails)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=YOUR_SENDGRID_API_KEY_HERE
DEFAULT_FROM_EMAIL=your-verified-email@yourdomain.com

# AI Services (for generating reports)
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
# If using Azure AI Foundry, also add:
# AZURE_OPENAI_ENDPOINT=your-azure-endpoint-url-here

# Reddit API (optional - for real customer reviews)
REDDIT_CLIENT_ID=your-reddit-client-id-here
REDDIT_CLIENT_SECRET=your-reddit-client-secret-here
REDDIT_USER_AGENT=YourAppName/1.0

# Security keys (generate random strings using commands below)
API_SECRET_KEY=some-random-string-here-make-it-unique
```

**Important Notes**:
- Replace `YOUR_SENDGRID_API_KEY_HERE` with your SendGrid API key from the steps above
- Replace `YOUR_OPENAI_API_KEY_HERE` with your OpenAI or Azure AI key
- For `DEFAULT_FROM_EMAIL`, use an email you've verified in SendGrid
- Reddit keys are optional - the system works without them

### **Step 4: Set Up the Database**

**What we're doing**: Creating a place to store our data (like creating filing cabinets)

```bash
# Still in the Agent1/django-backend folder
# This creates the database structure
python manage.py migrate

# Optional: Create an admin account for yourself
python manage.py createsuperuser
```

**For the superuser**: 
- Choose a username (like: john_smith)
- Enter your email
- Choose a password (write it down!)

### **Step 5: Set Up the Frontend (The Website Interface)**

**What we're doing**: Setting up the visual part that users interact with

1. **Open a NEW command prompt/terminal window** (keep the old one open)

2. **Navigate to the React folder**:
   ```bash
   # From the main Echo-Project folder
   cd React
   ```

3. **Install the required packages**:
   ```bash
   # This downloads all the website components we need
   npm install
   ```
   
   **What this does**: Downloads JavaScript libraries needed for our dashboard interface.

### **Step 6: Start Both Servers**

**What we're doing**: Starting both parts of our system

You'll need **TWO terminal/command prompt windows** open:

**Terminal 1 - Backend Server**:
```bash
# Navigate to backend folder
cd Agent1/django-backend

# Make sure virtual environment is activated (you should see (venv))
# If not, run: venv\Scripts\activate (Windows) or source venv/bin/activate (Mac)

# Start the backend server
python manage.py runserver
```

**Terminal 2 - Frontend Server**:
```bash
# Navigate to React folder  
cd React

# Start the frontend server
npm run dev
```

**Success indicators**:
- Backend: Should say "Starting development server at http://127.0.0.1:8000/"
- Frontend: Should say "Local: http://localhost:3000"

### **Step 7: Access the Application**

**What we're doing**: Opening our application in a web browser

Open your web browser and visit these addresses:

- **📊 Main Dashboard**: [http://localhost:3000](http://localhost:3000)
  - This is the main interface where users view intelligence reports
  
- **🔧 API Backend**: [http://localhost:8000](http://localhost:8000)
  - This shows that the backend is running
  
- **👨‍💼 Admin Panel**: [http://localhost:8000/admin](http://localhost:8000/admin)
  - Use the superuser account you created to log in here

---

## 🔧 How to Generate Required Security Keys

**What these are**: Random strings that keep our application secure

### **Generate SECRET_KEY**:
```bash
# Run this command to generate a secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Generate API_SECRET_KEY**:
```bash
# Run this command to generate an API secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**What to do**: Copy the output from these commands and paste them into your `.env` file.

---

## 🛠️ Common Problems & How to Fix Them

*Don't panic if something doesn't work! Here are solutions to common issues:*

### **❌ Problem: "Port already in use" or "Address already in use"**

**What this means**: Another program is using the same "address" as our application.

**How to fix**:

**For Windows**:
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID_NUMBER> with the number you see)
taskkill /PID <PID_NUMBER> /F
```

**For Mac/Linux**:
```bash
# Kill anything using port 8000
lsof -ti:8000 | xargs kill -9
```

**Simple alternative**: Restart your computer and try again.

### **❌ Problem: "Module not found" or "No module named..."**

**What this means**: Python can't find the libraries our project needs.

**How to fix**:
1. **Check if your virtual environment is active**:
   - Look for `(venv)` at the start of your command line
   - If you don't see it, run:
     ```bash
     # Windows
     venv\Scripts\activate
     
     # Mac/Linux  
     source venv/bin/activate
     ```

2. **Reinstall the packages**:
   ```bash
   pip install -r requirements.txt
   ```

### **❌ Problem: Database errors or "no such table"**

**What this means**: The database structure is missing or corrupted.

**How to fix**:
```bash
# Delete the old database (don't worry, this is safe in development)
rm db.sqlite3              # Mac/Linux
del db.sqlite3             # Windows

# Create a fresh database
python manage.py migrate

# Create a new admin user
python manage.py createsuperuser
```

### **❌ Problem: "npm install" fails or package errors**

**What this means**: The JavaScript packages didn't install correctly.

**How to fix**:
```bash
# Clear the cache and start fresh
npm cache clean --force

# Remove old files
rm -rf node_modules package-lock.json     # Mac/Linux
rmdir /s node_modules & del package-lock.json  # Windows

# Try installing again
npm install
```

### **❌ Problem: "Command not found" (python, npm, git, etc.)**

**What this means**: Your computer doesn't know where to find these programs.

**How to fix**:
1. **Restart your computer** (this often fixes PATH issues)
2. **Reinstall the software** and make sure to check "Add to PATH" during installation
3. **For Python specifically**: 
   - Uninstall and reinstall Python
   - ✅ **CRUCIAL**: Check "Add Python to PATH" during installation

### **❌ Problem: Nothing happens when I visit localhost:3000 or localhost:8000**

**What this means**: The servers aren't running or started incorrectly.

**How to fix**:
1. **Check both terminal windows are still running**
2. **Look for error messages** in the terminals
3. **Restart both servers**:
   - Press `Ctrl+C` in each terminal to stop
   - Run the start commands again
4. **Try different browsers** (Chrome, Firefox, Safari)

---

## ✅ How to Test Everything is Working

*Follow these steps to make sure everything is set up correctly:*

### **Test 1: Backend Server**
1. Visit: [http://localhost:8000/admin](http://localhost:8000/admin)
2. **Should see**: Django admin login page
3. **If you see this**: ✅ Backend is working!

### **Test 2: Frontend Dashboard**
1. Visit: [http://localhost:3000](http://localhost:3000)
2. **Should see**: The Intelligence Dashboard with blue shield logos
3. **If you see this**: ✅ Frontend is working!

### **Test 3: Database Connection**
1. Open a new terminal in the `Agent1/django-backend` folder
2. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac)
3. Run:
   ```bash
   python manage.py shell
   ```
4. Type:
   ```python
   from research_agent.models import ReportSubscription
   print("Database working!")
   exit()
   ```
5. **Should see**: "Database working!" message

### **Test 4: Email System** (Optional)
```bash
# In django-backend folder with venv activated
python send_email_now.py
```

---

## 🆘 Still Having Problems?

### **Step 1: Read Error Messages Carefully**
- Error messages usually tell you exactly what's wrong
- Copy the exact error message when asking for help

### **Step 2: Try These Universal Fixes**
1. **Restart your computer** - Fixes many environment issues
2. **Close all terminals and start fresh**
3. **Make sure virtual environment is activated** - Look for `(venv)`
4. **Update all packages**:
   ```bash
   pip install -r requirements.txt --upgrade
   npm install
   ```

### **Step 3: Ask for Help**
When asking for help, include:
- **What step you were on** when the error happened
- **The exact error message** (copy and paste it)
- **Your operating system** (Windows 10, Mac, etc.)
- **Screenshots** of the error

**Where to get help**:
- 💬 **Team chat** - Fastest response
- 📧 **GitHub Issues** - Create an issue at [https://github.com/Tokelowo/Echo-Project/issues](https://github.com/Tokelowo/Echo-Project/issues)
- � **Message team lead** directly with screenshots

---

## 🎯 Understanding What Each Part Does

*Don't worry about understanding all the technical details, but here's a simple explanation:*

### **🧠 Django Backend (Port 8000)**: 
- **What it does**: The "brain" of our system
- **Handles**: 
  - Storing data in the database
  - Generating intelligence reports using AI
  - Sending emails to subscribers
  - Processing API requests from the frontend

### **💻 React Frontend (Port 3000)**:
- **What it does**: The "face" of our system (what users see)
- **Handles**:
  - Showing the dashboard with charts and data
  - Letting users subscribe to reports
  - Displaying intelligence information in a user-friendly way
  - Handling button clicks and user interactions

### **📧 SendGrid Email Service**:
- **What it does**: Professional email delivery system
- **Handles**:
  - Sending beautifully formatted intelligence reports
  - Managing email subscriptions
  - Tracking email delivery success
  - Ensuring emails don't go to spam

### **🗄️ SQLite Database**:
- **What it does**: File-based storage system (like a digital filing cabinet)
- **Stores**:
  - User subscription preferences
  - Generated reports and their data
  - Email delivery logs
  - User accounts and settings

---

## 📚 Helpful Resources for Beginners

### **Learn More About the Technologies We Use**:
- **Python**: [https://www.python.org/about/gettingstarted/](https://www.python.org/about/gettingstarted/)
- **Django**: [https://www.djangoproject.com/start/](https://www.djangoproject.com/start/)
- **React**: [https://react.dev/learn](https://react.dev/learn)
- **Git**: [https://try.github.io/](https://try.github.io/)

### **Command Line Tutorials**:
- **Windows Command Prompt**: [https://www.computerhope.com/issues/chusedos.htm](https://www.computerhope.com/issues/chusedos.htm)
- **Mac Terminal**: [https://support.apple.com/guide/terminal/welcome/mac](https://support.apple.com/guide/terminal/welcome/mac)

### **VS Code Setup**:
- **Download**: [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **Python Extension**: [https://marketplace.visualstudio.com/items?itemName=ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

---

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

*Once you have everything set up, here's how to work on the project every day:*

### **🌅 Starting Your Work Day:**

**Every time you want to work on the project, follow these steps:**

1. **Open TWO terminal/command prompt windows**

2. **Terminal 1 - Start the Backend**:
   ```bash
   # Navigate to the backend folder
   cd Documents/Echo-Project/Agent1/django-backend
   
   # Activate the virtual environment (IMPORTANT!)
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # Mac/Linux
   
   # You should see (venv) at the start of your command line
   
   # Start the backend server
   python manage.py runserver
   ```
   
   **Success**: Should show "Starting development server at http://127.0.0.1:8000/"

3. **Terminal 2 - Start the Frontend**:
   ```bash
   # Navigate to the frontend folder
   cd Documents/Echo-Project/React
   
   # Start the frontend server
   npm run dev
   ```
   
   **Success**: Should show "Local: http://localhost:3000"

4. **Open your browser** and go to [http://localhost:3000](http://localhost:3000)

### **✏️ Making Changes to the Code:**

**Backend Changes** (Python/Django):
- **Where to edit**: Files in `Agent1/django-backend/research_agent/`
- **Common files you might edit**:
  - `views.py` - Controls what data the API returns
  - `models.py` - Defines database structure
  - `email_service.py` - Handles email sending
- **After making changes**: The server automatically restarts (usually)

**Frontend Changes** (React/JavaScript):
- **Where to edit**: Files in `React/src/`
- **Common files you might edit**:
  - `src/pages/Dashboard.jsx` - Main dashboard page
  - `src/components/` - Reusable UI components
  - `src/styles/` - Styling and appearance
- **After making changes**: The page automatically refreshes in your browser

**Database Changes** (if you modify models.py):
```bash
# In the backend terminal (with venv activated)
python manage.py makemigrations
python manage.py migrate
```

### **💾 Saving Your Work (Git Commands):**

**When you've made changes and want to save them:**

1. **Check what you've changed**:
   ```bash
   git status
   ```
   
2. **Add your changes**:
   ```bash
   # Add all changes
   git add .
   
   # OR add specific files
   git add filename.py
   ```

3. **Commit (save) your changes**:
   ```bash
   git commit -m "Brief description of what you changed"
   ```
   
   **Example**: `git commit -m "Fixed email sending bug"`

4. **Push to GitHub** (share with team):
   ```bash
   git push origin master
   ```

### **📥 Getting Latest Changes from Team:**

**Before starting work each day, get the latest code:**

```bash
# Download latest changes from team
git pull origin master

# If backend requirements changed, update packages:
pip install -r requirements.txt

# If frontend packages changed, update:
npm install
```

### **🛑 Ending Your Work Day:**

1. **Save your work** (see "Saving Your Work" above)
2. **Stop both servers**:
   - Press `Ctrl+C` in each terminal window
3. **Close terminal windows**

---

## 🎯 Quick Reference - What Each Folder Contains

*Think of this like a filing system - everything has its place:*

```
Echo-Project/                    # 📁 Main project folder
├── Agent1/django-backend/       # 🧠 Backend (Python/Django)
│   ├── research_agent/          #   📊 Main business logic
│   │   ├── models.py           #     🗃️ Database structure
│   │   ├── views.py            #     🔗 API endpoints
│   │   └── email_service.py    #     📧 Email handling
│   ├── requirements.txt         #   📋 List of Python packages needed
│   ├── manage.py               #   🛠️ Django command runner
│   ├── .env                    #   ⚙️ Your personal settings
│   └── db.sqlite3              #   🗄️ Database file
│
├── React/                      # 💻 Frontend (React/JavaScript)
│   ├── src/                    #   📝 Source code
│   │   ├── pages/              #     📄 Main pages (Dashboard, etc.)
│   │   ├── components/         #     🧩 Reusable UI pieces
│   │   └── styles/             #     🎨 Visual styling
│   ├── package.json            #   📋 List of JavaScript packages
│   └── public/                 #   🌐 Static files (images, etc.)
│
├── .gitignore                  # � Files Git should ignore
├── README.md                   # 📖 Detailed project documentation
└── TEAM_SETUP.md              # 👥 This guide!
```

---

## � Congratulations!

**You're now ready to contribute to Echo Intelligence!**

### **What You Can Do Now**:
- ✅ Run the complete application locally
- ✅ Make changes to both frontend and backend
- ✅ Test your changes immediately
- ✅ Save and share your work with the team
- ✅ Troubleshoot common problems

### **Next Steps**:
1. **Explore the application** - Click around and see how it works
2. **Read the main README.md** - More detailed technical information
3. **Ask questions** - No question is too basic!
4. **Start with small changes** - Maybe update some text or colors first

### **Remember**:
- 💡 **It's okay to break things** - That's how you learn!
- 🆘 **Ask for help early** - Don't spend hours stuck on something
- 📚 **Save your work frequently** - Commit often
- 🎯 **Focus on one thing at a time** - Small changes are easier to test

---

**� Welcome to the Echo Intelligence team! You've got this!**

*Questions? Don't hesitate to ask - we're here to help you succeed!*
