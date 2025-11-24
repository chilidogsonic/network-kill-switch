@echo off
:: Batch file to remove Ethernet Toggle auto-startup
:: This must be run as Administrator

echo ========================================
echo Ethernet Toggle Auto-Startup Removal
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
echo Running removal script...
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0remove_startup.ps1"

if %errorLevel% equ 0 (
    echo.
    echo Removal completed successfully!
) else (
    echo.
    echo Removal failed! See error messages above.
)

echo.
pause
