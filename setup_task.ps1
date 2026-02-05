# Setup Windows Task Scheduler for Daily Stock Analysis at 9:30 AM

$taskName = "DailyStockAnalysisEmail"
$batchPath = "C:\Users\rohitkundu\OneDrive - Microsoft\Documents\Trade\run_email_analysis.bat"

# Remove existing task if present
schtasks /delete /tn $taskName /f 2>$null

# Create new task
$action = New-ScheduledTaskAction -Execute $batchPath
$trigger = New-ScheduledTaskTrigger -Daily -At "09:30AM"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Daily stock analysis at 9:30 AM with email report"

Write-Host ""
Write-Host "Task '$taskName' created successfully!" -ForegroundColor Green
Write-Host "Analysis will run daily at 9:30 AM" -ForegroundColor Cyan
Write-Host ""

# Show task status
schtasks /query /tn $taskName
