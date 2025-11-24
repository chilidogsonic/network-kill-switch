@echo off
:: Batch file to setup Ethernet Toggle auto-startup
:: This must be run as Administrator

echo ========================================
echo Ethernet Toggle Auto-Startup Setup
echo ========================================
echo.

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires Administrator privileges!
    echo.
    echo Please right-click this file and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

:: Run the PowerShell script
echo Running setup script...
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0setup_startup.ps1"

if %errorLevel% equ 0 (
    echo.
    echo Setup completed successfully!
) else (
    echo.
    echo Setup failed! See error messages above.
)

echo.
pause
