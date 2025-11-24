; Inno Setup Script for Ethernet Toggle Application
; Requires Inno Setup 6.0 or later: https://jrsoftware.org/isinfo.php

#define MyAppName "Ethernet Toggle"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Ethernet Toggle"
#define MyAppURL "https://github.com/yourusername/ethernet-toggle"
#define MyAppExeName "EthernetToggle.exe"

[Setup]
; Application information
AppId={{8E9F7A3B-4D2C-4F5E-9A1B-6C8D3E4F5A6B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output
OutputDir=Output
OutputBaseFilename=EthernetToggle-Setup
Compression=lzma
SolidCompression=yes

; Privileges - required for creating scheduled tasks
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Visual
WizardStyle=modern
; SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compatibility
MinVersion=10.0
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "startauto"; Description: "Start {#MyAppName} automatically when Windows starts (recommended)"; GroupDescription: "Startup Options:"; Flags: checkedonce

[Files]
; Main executable (will be built by PyInstaller)
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; PowerShell scripts for auto-startup
Source: "setup_task_silent.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "uninstall_task.ps1"; DestDir: "{app}"; Flags: ignoreversion
; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
; Create Start Menu shortcut
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Toggle Ethernet adapter on/off"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

[Run]
; Option to launch application after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent shellexec

[Code]
// Function to execute PowerShell script for auto-startup setup
procedure SetupAutoStart();
var
  ResultCode: Integer;
  ScriptPath: String;
  InstallPath: String;
  PowerShellCmd: String;
begin
  ScriptPath := ExpandConstant('{app}\setup_task_silent.ps1');
  InstallPath := ExpandConstant('{app}');
  PowerShellCmd := Format('-ExecutionPolicy Bypass -File "%s" -InstallPath "%s"', [ScriptPath, InstallPath]);

  Exec('powershell.exe', PowerShellCmd, '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  // Ignore errors - don't block installation if auto-start setup fails
end;

// Function to remove scheduled task during uninstallation
procedure RemoveAutoStart();
var
  ResultCode: Integer;
  ScriptPath: String;
  PowerShellCmd: String;
begin
  ScriptPath := ExpandConstant('{app}\uninstall_task.ps1');
  PowerShellCmd := Format('-ExecutionPolicy Bypass -File "%s"', [ScriptPath]);

  Exec('powershell.exe', PowerShellCmd, '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  // Ignore errors - don't block uninstallation
end;

// Called after installation is complete
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // If user checked the auto-start option, configure it
    if WizardIsTaskSelected('startauto') then
    begin
      SetupAutoStart();
    end;
  end;
end;

// Called during uninstallation
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    // Remove scheduled task if it exists
    RemoveAutoStart();
  end;
end;
