# Setup Daily Report Email Task
# This script creates a scheduled task to send daily reports at 11 PM

# Define task parameters
$TaskName = "SmartBusiness_DailyReport"
$ScriptPath = "E:\AI\send_daily_report.bat"
$Time = "23:00"  # 11:00 PM

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "Task already exists. Updating..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create the scheduled task action
$Action = New-ScheduledTaskAction -Execute $ScriptPath

# Create the scheduled task trigger (daily at 11 PM)
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time

# Create the scheduled task settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Create the principal (run as current user)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Register the scheduled task
try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Send daily business reports for all accounts via email"
    Write-Host "Scheduled task '$TaskName' created successfully!" -ForegroundColor Green
    Write-Host "The daily reports for all accounts will be sent every day at 11:00 PM" -ForegroundColor Yellow
} catch {
    Write-Host "Failed to create scheduled task: $($_.Exception.Message)" -ForegroundColor Red
}

# Show task information
Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State, Actions, Triggers