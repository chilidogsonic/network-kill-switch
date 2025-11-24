# Silent PowerShell Script for Uninstaller - Remove Ethernet Toggle Auto-Startup
# This is called by the Inno Setup uninstaller to remove the scheduled task

$ErrorActionPreference = "Stop"
$TaskName = "EthernetToggleApp"

try {
    # Check if task exists
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

    if ($existingTask) {
        # Remove the task
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false | Out-Null
    }

    exit 0

} catch {
    # Silent failure - don't block uninstallation
    Write-EventLog -LogName Application -Source "Application" -EntryType Warning -EventId 1001 -Message "Failed to remove Ethernet Toggle scheduled task: $($_.Exception.Message)" -ErrorAction SilentlyContinue
    exit 0  # Exit with success anyway to not block uninstall
}
