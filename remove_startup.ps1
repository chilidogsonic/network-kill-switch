# PowerShell Script to Remove Ethernet Toggle App Auto-Startup
# This removes the scheduled task

$ErrorActionPreference = "Stop"

$TaskName = "EthernetToggleApp"

Write-Host "=== Ethernet Toggle Auto-Startup Removal ===" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Check if task exists
Write-Host "Checking for scheduled task '$TaskName'..." -ForegroundColor Yellow
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if (-not $existingTask) {
    Write-Host ""
    Write-Host "Task '$TaskName' not found." -ForegroundColor Yellow
    Write-Host "Auto-startup is not currently configured." -ForegroundColor Gray
    Write-Host ""
    exit 0
}

# Remove the task
try {
    Write-Host "Removing scheduled task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false

    Write-Host ""
    Write-Host "SUCCESS! Auto-startup has been removed." -ForegroundColor Green
    Write-Host ""
    Write-Host "The Ethernet Toggle app will no longer start automatically at login." -ForegroundColor Cyan
    Write-Host "You can still run it manually using run_ethernet_toggle.bat" -ForegroundColor Gray
    Write-Host ""
    Write-Host "To re-enable auto-startup, run: setup_startup.bat" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to remove scheduled task!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
