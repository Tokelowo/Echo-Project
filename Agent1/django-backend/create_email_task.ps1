# PowerShell script to create daily email scheduled task
$TaskName = "DailyEmailReports"
$ScriptPath = "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend\send_daily_emails_improved.bat"

Write-Host "Creating scheduled task: $TaskName"
Write-Host "Script path: $ScriptPath"

# Remove existing task if it exists
try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Removed existing task"
} catch {
    Write-Host "No existing task to remove"
}

# Create task components
$Action = New-ScheduledTaskAction -Execute $ScriptPath
$Trigger = New-ScheduledTaskTrigger -Daily -At "09:00"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

# Register the task
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal

Write-Host "✅ Scheduled task '$TaskName' created successfully!"
Write-Host "📅 Will run daily at 9:00 AM"
Write-Host "📁 Script: $ScriptPath"

# Test the task
Write-Host "`n🧪 Testing task manually..."
try {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "✅ Task started successfully!"
} catch {
    Write-Host "❌ Error starting task: $($_.Exception.Message)"
}

Write-Host "`n🎉 Email system setup complete!"
Write-Host "Your daily emails will be sent every morning at 9:00 AM."
