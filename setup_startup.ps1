# PowerShell Script to Setup Ethernet Toggle App Auto-Startup
# This creates a scheduled task that runs at user logon with elevated privileges

$ErrorActionPreference = "Stop"

$TaskName = "EthernetToggleApp"
$AppPath = $PSScriptRoot

Write-Host "=== Ethernet Toggle Auto-Startup Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Find Python executable
Write-Host "Searching for Python installation..." -ForegroundColor Yellow
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) {
    Write-Host "ERROR: Python not found in PATH!" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and added to PATH." -ForegroundColor Yellow
    exit 1
}

# Get pythonw.exe path (same directory as python.exe)
$pythonDir = Split-Path $pythonPath -Parent
$pythonwPath = Join-Path $pythonDir "pythonw.exe"

if (-not (Test-Path $pythonwPath)) {
    Write-Host "ERROR: pythonw.exe not found at: $pythonwPath" -ForegroundColor Red
    Write-Host "Using python.exe instead (console window may appear)" -ForegroundColor Yellow
    $pythonwPath = $pythonPath
}

Write-Host "Found Python: $pythonwPath" -ForegroundColor Green

# Check if ethernet_toggle.py exists
$scriptPath = Join-Path $AppPath "ethernet_toggle.py"
if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: ethernet_toggle.py not found at: $scriptPath" -ForegroundColor Red
    exit 1
}

Write-Host "Found script: $scriptPath" -ForegroundColor Green
Write-Host ""

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Task '$TaskName' already exists." -ForegroundColor Yellow
    $response = Read-Host "Do you want to replace it? (y/n)"
    if ($response -ne 'y') {
        Write-Host "Setup cancelled." -ForegroundColor Yellow
        exit 0
    }
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create scheduled task action
Write-Host "Creating scheduled task..." -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute $pythonwPath -Argument "`"$scriptPath`"" -WorkingDirectory $AppPath

# Create trigger for user logon
$trigger = New-ScheduledTaskTrigger -AtLogOn

# Create principal (run with highest privileges)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest

# Create settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 0)

# Register the task
try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description "Auto-start Ethernet Toggle system tray application" | Out-Null

    Write-Host ""
    Write-Host "SUCCESS! Auto-startup has been configured." -ForegroundColor Green
    Write-Host ""
    Write-Host "The Ethernet Toggle app will now start automatically when you log in." -ForegroundColor Cyan
    Write-Host "It will run silently in the system tray without any UAC prompts." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To verify, check Task Scheduler or restart your computer." -ForegroundColor Gray
    Write-Host "To disable auto-startup, run: remove_startup.bat" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to create scheduled task!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
