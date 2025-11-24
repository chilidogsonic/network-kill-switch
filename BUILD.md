# Building the Ethernet Toggle Installer

This document explains how to build a standalone installer for the Ethernet Toggle application.

## Prerequisites

### Required Software

1. **Python 3.7 or higher**
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Inno Setup 6.0 or higher**
   - Download from: https://jrsoftware.org/isinfo.php
   - Required for creating the Windows installer
   - Install to the default location

### Python Dependencies

The build script will automatically install these, but you can install manually:

```bash
pip install -r requirements.txt
pip install pyinstaller
```

## Building the Installer

### Automated Build (Recommended)

Simply run the automated build script:

```bash
build_installer.bat
```

This script will:
1. Check for Python installation
2. Install/upgrade PyInstaller
3. Install application dependencies
4. Build standalone executable with PyInstaller
5. Check for Inno Setup
6. Compile the installer with Inno Setup

### Build Output

After successful build:
- **Standalone executable:** `dist\EthernetToggle.exe` (~15-25 MB)
- **Installer package:** `Output\EthernetToggle-Setup.exe` (~20-30 MB)

The installer is what you distribute to users.

## Manual Build Steps

If you need to build manually or troubleshoot issues:

### Step 1: Build Standalone Executable

```bash
# Without icon
pyinstaller --onefile --windowed --name "EthernetToggle" ethernet_toggle.py

# With icon (if icon.ico exists)
pyinstaller --onefile --windowed --name "EthernetToggle" --icon="icon.ico" ethernet_toggle.py
```

This creates `dist\EthernetToggle.exe`

### Step 2: Test the Executable

Before creating the installer, test the standalone executable:

```bash
dist\EthernetToggle.exe
```

The app should:
- Start without errors
- Appear in system tray
- Toggle Ethernet adapter successfully
- Run with admin privileges

### Step 3: Compile Installer

Using Inno Setup GUI:
1. Open Inno Setup
2. File → Open → Select `installer.iss`
3. Build → Compile
4. Output will be in `Output\EthernetToggle-Setup.exe`

Using command line:
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

## Troubleshooting

### PyInstaller Issues

**"Module not found" errors:**
- Install missing dependencies: `pip install <module-name>`
- Check that all imports in `ethernet_toggle.py` are satisfied

**Executable is too large (>50 MB):**
- Normal size is 20-30 MB
- PyInstaller bundles Python runtime and dependencies
- Consider using `--onedir` instead of `--onefile` to see what's included

**Antivirus false positives:**
- PyInstaller executables may trigger antivirus warnings
- This is common with PyInstaller-built applications
- Consider code signing (requires a certificate)
- Test with Windows Defender

**Console window appears:**
- Make sure you're using `--windowed` or `-w` flag
- Check that `pythonw.exe` is being used in the spec file

### Inno Setup Issues

**"Cannot find file: dist\EthernetToggle.exe":**
- Make sure PyInstaller step completed successfully
- Check that `dist\EthernetToggle.exe` exists
- Build the executable first before running Inno Setup

**PowerShell scripts fail during installation:**
- Ensure `setup_task_silent.ps1` and `uninstall_task.ps1` exist
- Check PowerShell execution policy on target system
- Scripts use `-ExecutionPolicy Bypass` to avoid issues

**Installer requires admin but doesn't prompt:**
- This is correct behavior - installer needs admin for Program Files
- User will see UAC prompt when running installer
- After installation, app runs without UAC due to scheduled task

## Customization

### Change Application Version

Edit `installer.iss`:
```pascal
#define MyAppVersion "1.0.0"
```

### Change Application Icon

1. Create or download a `.ico` file with multiple sizes (16x16, 32x32, 48x48, 256x256)
2. Save as `icon.ico` in the project directory
3. Rebuild with `build_installer.bat`

The icon will be used for:
- Application executable
- System tray icon (drawn programmatically, not from .ico)
- Installer icon
- Start Menu shortcut

### Change Installation Directory

Edit `installer.iss`:
```pascal
DefaultDirName={autopf}\YourAppName
```

### Add/Remove Files from Installer

Edit the `[Files]` section in `installer.iss`:
```pascal
[Files]
Source: "yourfile.txt"; DestDir: "{app}"; Flags: ignoreversion
```

## Distribution

### What to Distribute

Distribute **only** the installer:
- `Output\EthernetToggle-Setup.exe`

Users do **not** need:
- Python
- Any dependencies
- Source code
- Other project files

### Testing the Installer

Before distributing, test on a clean system:

1. **Virtual Machine (Recommended):**
   - Create a clean Windows 10/11 VM
   - Install the app using the installer
   - Test all functionality
   - Test uninstallation

2. **Test Checklist:**
   - [ ] Installer runs and shows wizard
   - [ ] Auto-startup checkbox appears
   - [ ] Installation completes successfully
   - [ ] App appears in Start Menu
   - [ ] App appears in Programs & Features
   - [ ] App starts and works correctly
   - [ ] Auto-startup works (if enabled)
   - [ ] Uninstaller removes everything
   - [ ] Scheduled task is removed on uninstall

### File Sharing

Share the installer via:
- Direct download (GitHub Releases, Dropbox, Google Drive, etc.)
- Company intranet
- USB drive
- Email (if size permits)

**Note:** Some email providers may block `.exe` files. Consider:
- Renaming to `.ex_` and instructing users to rename back
- Compressing to `.zip` file
- Using cloud storage links instead

## Advanced: Code Signing

To avoid "Unknown Publisher" warnings:

1. **Obtain a code signing certificate**
   - Purchase from certificate authority (Sectigo, DigiCert, etc.)
   - Cost: ~$100-500/year
   - Requires business verification

2. **Sign the executable**
   ```bash
   signtool sign /f "certificate.pfx" /p "password" /t http://timestamp.digicert.com dist\EthernetToggle.exe
   ```

3. **Sign the installer**
   ```bash
   signtool sign /f "certificate.pfx" /p "password" /t http://timestamp.digicert.com Output\EthernetToggle-Setup.exe
   ```

Code signing is optional but recommended for professional distribution.

## Version Control

When committing to Git, add to `.gitignore`:
```
build/
dist/
Output/
*.spec
__pycache__/
*.pyc
```

Keep in version control:
- Source code (`.py` files)
- Build scripts (`.bat`, `.ps1`)
- Installer configuration (`installer.iss`)
- Documentation (`.md` files)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Try a clean build (delete `build/`, `dist/`, `Output/` folders)
4. Check PyInstaller documentation: https://pyinstaller.org/
5. Check Inno Setup documentation: https://jrsoftware.org/ishelp/
