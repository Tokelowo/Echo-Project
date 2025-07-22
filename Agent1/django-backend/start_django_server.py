import os
import subprocess
import sys

# Change to Django directory
os.chdir(r"c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend")
print(f"Changed directory to: {os.getcwd()}")

# Start Django server
print("Starting Django server on port 8000...")
subprocess.run([sys.executable, "manage.py", "runserver", "8000"])
