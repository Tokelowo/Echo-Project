#!/usr/bin/env python
"""
Setup automated email delivery using Windows Task Scheduler
This will create a batch file and set up automatic daily email delivery
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def setup_automated_email_delivery():
    """Set up automated email delivery system"""
    
    print("🔧 Setting up automated email delivery system...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create batch file for automated execution
    batch_content = f'''@echo off
cd /d "{current_dir}"
python manage.py send_scheduled_reports
echo Email delivery completed at %date% %time%
'''
    
    batch_file_path = os.path.join(current_dir, "automated_email_delivery.bat")
    
    with open(batch_file_path, 'w') as f:
        f.write(batch_content)
    
    print(f"✅ Created batch file: {batch_file_path}")
    
    # Create PowerShell script for Windows Task Scheduler
    ps_content = f'''# PowerShell script to create Windows scheduled task for email delivery
$taskName = "EchoProject_EmailDelivery"
$batchFile = "{batch_file_path}"
$trigger = New-ScheduledTaskTrigger -Daily -At "9:00 AM"
$action = New-ScheduledTaskAction -Execute $batchFile
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Remove existing task if it exists
try {{
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Output "Removed existing task"
}} catch {{
    Write-Output "No existing task to remove"
}}

# Create new scheduled task
Register-ScheduledTask -TaskName $taskName -Trigger $trigger -Action $action -Settings $settings -Description "Automated email delivery for Echo Project intelligence reports"

Write-Output "✅ Scheduled task '$taskName' created successfully!"
Write-Output "✅ Will run daily at 9:00 AM"
Write-Output "✅ Batch file: $batchFile"
'''
    
    ps_file_path = os.path.join(current_dir, "setup_scheduled_task.ps1")
    
    with open(ps_file_path, 'w') as f:
        f.write(ps_content)
    
    print(f"✅ Created PowerShell script: {ps_file_path}")
    
    print("\n🚀 AUTOMATION SETUP INSTRUCTIONS:")
    print("1. Run the PowerShell script as Administrator to set up the scheduled task:")
    print(f"   PowerShell -ExecutionPolicy Bypass -File \"{ps_file_path}\"")
    print("\n2. Or manually run the batch file to test:")
    print(f"   \"{batch_file_path}\"")
    
    return batch_file_path, ps_file_path

if __name__ == "__main__":
    setup_automated_email_delivery()
