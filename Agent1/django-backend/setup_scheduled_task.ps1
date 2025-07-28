# PowerShell script to create Windows scheduled task for email delivery
$taskName = "EchoProject_EmailDelivery"
$batchFile = "c:\Users\t-tokelowo\Documents\Echo Project\Agent1\django-backend\automated_email_delivery.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At "9:00 AM"
$action = New-ScheduledTaskAction -Execute $batchFile
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Remove existing task if it exists
try {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Output "Removed existing task"
} catch {
    Write-Output "No existing task to remove"
}

# Create new scheduled task
Register-ScheduledTask -TaskName $taskName -Trigger $trigger -Action $action -Settings $settings -Description "Automated email delivery for Echo Project intelligence reports"

Write-Output "SUCCESS: Scheduled task '$taskName' created successfully!"
Write-Output "SUCCESS: Will run daily at 9:00 AM"
Write-Output "SUCCESS: Batch file: $batchFile"
