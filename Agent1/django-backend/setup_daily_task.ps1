# PowerShell script to set up daily email task
$ScriptPath = "c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend\send_daily_emails.bat"
$TaskName = "DailyEmailReports"
$Time = "09:00"

# Delete existing task if it exists
try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Removed existing task: $TaskName"
} catch {
    Write-Host "No existing task to remove"
}

# Create new scheduled task
$Action = New-ScheduledTaskAction -Execute $ScriptPath
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal

Write-Host "✅ Created scheduled task: $TaskName"
Write-Host "📅 Will run daily at: $Time"
Write-Host "📁 Script location: $ScriptPath"

# Run it once manually to test
Write-Host "`n🧪 Testing task manually..."
Start-ScheduledTask -TaskName $TaskName

Write-Host "`n🎉 Daily email system restored!"
Write-Host "Your daily emails will now be sent every morning at 9:00 AM."
