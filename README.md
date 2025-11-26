# Network Kill Switch

<p align="center">
  <img src="assets/logofor_readme.png" alt="Network Kill Switch Logo" width="100%"/>
</p>

<p align="center">
  <strong>A lightweight Windows system tray application for instant network control</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Windows-10%2F11-blue?logo=windows" alt="Windows 10/11"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License"/>
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue?logo=python" alt="Python 3.7+"/>
  <img src="https://img.shields.io/badge/version-2.0.0-orange" alt="Version 2.0.0"/>
</p>

## What is Network Kill Switch?

Network Kill Switch is a powerful yet simple Windows utility that gives you instant control over your network connections. With a single click from your system tray, you can disable or enable all network adapters (Ethernet and WiFi) simultaneously. Perfect for privacy, security, focus time, or quick network troubleshooting.

## Features

- **System Tray Integration** - Lives quietly in your Windows system tray
- **One-Click Toggle** - Left-click icon to instantly toggle all network adapters
- **Visual Status Indicators** - Green = network enabled, Red = network disabled
- **Complete Network Control** - Toggles both Ethernet AND WiFi adapters together
- **Smart Timer Function** - Temporarily disable network with auto-restore:
  - 1 minute
  - 2 minutes
  - 5 minutes
  - 30 minutes
  - 1 hour
- **Live Countdown Display** - See remaining time in real-time on the tray icon tooltip
- **Loading Animation** - Visual feedback during network state changes
- **Status Verification** - Automatically verifies adapter state after toggling
- **Auto-Detection** - Finds your physical network adapters automatically
- **Auto-Startup** - Optional "Start with Windows" during installation
- **Standalone Installer** - No Python installation required
- **ARM Compatible** - Works on Windows on ARM via x64 emulation
- **Lightweight** - Minimal resource usage (~20-30 MB installed)

## Screenshots

### System Tray - Network Enabled (Green)
![Network Enabled](screenshots/network_on.png)

### System Tray - Network Disabled (Red)
![Network Disabled](screenshots/network_off.png)

### Timer Options Menu
![Timer Options](screenshots/timer_options.png)

## Download & Installation

### For End Users

**[Download Latest Release (v2.0.0)](https://github.com/chilidogsonic/network-kill-switch/releases/latest)**

1. **Download** `NetworkKillSwitch-Setup.exe` from the [Releases](https://github.com/chilidogsonic/network-kill-switch/releases) page
2. **Run the installer** (requires administrator privileges)
3. **Follow the installation wizard:**
   - Choose your installation directory (default: `C:\Program Files\Network Kill Switch`)
   - Check "Start with Windows" to enable automatic startup (recommended)
   - Click **Install**
4. **Done!** The app will appear in your system tray immediately

**No Python installation required!** The installer includes everything you need.

### Uninstallation

1. Open **Windows Settings** → **Apps** → **Installed apps**
2. Find **"Network Kill Switch"**
3. Click **Uninstall**

The uninstaller will automatically:
- Stop any running instances
- Remove the auto-startup configuration
- Clean up all files and registry entries

## Usage Guide

### Quick Start

1. **Find the icon** in your system tray (notification area, bottom-right corner)
   - **Green icon** = Network enabled (at least one adapter is active)
   - **Red icon** = Network disabled (all adapters are off)
   - **Timer icon** = Temporary disable mode (will auto-restore)

2. **Quick Actions:**
   - **Left-click** the icon → Instantly toggle all network adapters on/off
   - **Right-click** the icon → Open full menu with advanced options

### Menu Options (Right-Click)

- **Toggle Network (On/Off)** - Enable or disable ALL network adapters
- **Disable for 1/2/5/30/60 minutes** - Temporary disable with automatic restore
- **Cancel Timer** - Stop countdown and restore network immediately
- **Quit** - Exit the application

### Timer Feature

When you select a timer option:
1. All network adapters are immediately disabled
2. The tray icon changes to the timer icon
3. **Hover over the icon** to see a live countdown (e.g., "Network: Disabled (Re-enabling in 4m 32s)")
4. The network automatically restores when the timer expires
5. You can click "Cancel Timer" or manually toggle to restore early

### Tips

- **Keyboard shortcuts:** Not currently supported, but you can assign a hotkey to the executable via Windows properties
- **Multiple adapters:** The app detects and controls ALL physical Ethernet and WiFi adapters simultaneously
- **Virtual adapters:** VPN, Hyper-V, and other virtual adapters are excluded from control
- **Administrator required:** The app must run with admin privileges to control network adapters

## For Developers

### System Requirements

- **OS:** Windows 10 or Windows 11
- **Python:** 3.7 or higher (for development only)
- **Privileges:** Administrator rights (required to toggle network adapters)

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/chilidogsonic/network-kill-switch.git
   cd network-kill-switch
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # Open Command Prompt or PowerShell as Administrator
   python network_kill_switch.py
   ```

   The app will appear in your system tray.

### Building from Source

Want to build your own installer? See [BUILD.md](BUILD.md) for detailed instructions.

**Quick Build:**
```bash
# Install dependencies
pip install -r requirements.txt

# Build the standalone EXE and installer
build_installer.bat
```

**Output:**
- Standalone EXE: `dist\NetworkKillSwitch.exe`
- Windows Installer: `Output\NetworkKillSwitch-Setup.exe`

### Build Prerequisites

- Python 3.7+
- [Inno Setup 6](https://jrsoftware.org/isinfo.php) (for creating the installer)
- PyInstaller (automatically installed by build script)

## Troubleshooting

<details>
<summary><b>"Could not find network adapter" error</b></summary>

**Solution:**
- The app looks for physical Ethernet and WiFi adapters using specific naming patterns
- Virtual adapters (VPN, Hyper-V, VMware, VirtualBox) are intentionally excluded
- Check your adapter names in **Device Manager** → **Network adapters**
- If your adapter has an unusual name, you may need to modify the detection logic in `network_kill_switch.py` (line 131)
</details>

<details>
<summary><b>Toggle doesn't work / No effect when clicking</b></summary>

**Solution:**
1. **Verify administrator privileges:**
   - Press `Ctrl+Shift+Esc` to open Task Manager
   - Find `NetworkKillSwitch.exe` in the Details tab
   - Check if "Elevated" column shows "Yes"
   - If not, right-click the app shortcut → "Run as administrator"

2. **Check Windows Event Viewer:**
   - Press `Win+X` → Event Viewer
   - Navigate to **Windows Logs** → **System**
   - Look for errors related to network adapter operations

3. **Test PowerShell commands manually:**
   - Open PowerShell as Administrator
   - Run: `Get-NetAdapter` (should list your adapters)
   - Run: `Disable-NetAdapter -Name "Ethernet" -Confirm:$false` (replace "Ethernet" with your adapter name)
</details>

<details>
<summary><b>Auto-startup not working</b></summary>

**Solution:**
1. **Check Task Scheduler:**
   - Press `Win+R` → type `taskschd.msc` → Enter
   - Look for a task named **"NetworkKillSwitchApp"**
   - Right-click → **Properties** → Verify:
     - Trigger: "At log on"
     - Action: Points to correct EXE path
     - "Run with highest privileges" is checked

2. **Run diagnostic script:**
   - Navigate to installation folder: `C:\Program Files\Network Kill Switch`
   - Right-click `check_task_permissions.ps1` → "Run with PowerShell"
   - Review the diagnostic output

3. **Manual setup:**
   - Right-click `setup_task_silent.ps1` in the installation folder
   - Select "Run with PowerShell"
</details>

<details>
<summary><b>Icon doesn't appear in system tray</b></summary>

**Solution:**
1. **Check if app is running:**
   - Open Task Manager (`Ctrl+Shift+Esc`)
   - Look for `NetworkKillSwitch.exe` under "Background processes"

2. **Check overflow area:**
   - Click the **^** arrow in your system tray (hidden icons)
   - The icon might be collapsed there

3. **Restart the application:**
   - Kill the process in Task Manager
   - Relaunch from Start Menu or installation folder
</details>

<details>
<summary><b>App shows "Loading..." indefinitely</b></summary>

**Solution:**
- This usually indicates PowerShell commands are timing out
- Check your antivirus software isn't blocking PowerShell execution
- Try running as Administrator
- Verify PowerShell execution policy: `Get-ExecutionPolicy` (should be at least RemoteSigned)
</details>

## Technical Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.7+ | Core application logic |
| **UI Framework** | [pystray](https://github.com/moses-palmer/pystray) | System tray integration and menu |
| **Image Processing** | [Pillow (PIL)](https://pillow.readthedocs.io/) | Icon rendering and manipulation |
| **Network Control** | Windows PowerShell | Native adapter enable/disable commands |
| **Packaging** | [PyInstaller](https://pyinstaller.org/) | Standalone EXE compilation |
| **Installer** | [Inno Setup](https://jrsoftware.org/isinfo.php) | Windows installer creation |

### How It Works

1. **Adapter Detection:**
   - Uses PowerShell's `Get-NetAdapter` cmdlet to enumerate physical network adapters
   - Filters for Ethernet and WiFi adapters (excludes virtual adapters like VPN, Hyper-V)
   - Supports multiple adapters simultaneously

2. **State Management:**
   - Monitors adapter status using `Get-NetAdapter | Select-Object Status`
   - Real-time status verification after each toggle operation
   - Tooltip updates every second during timer countdown

3. **Toggle Operation:**
   - Executes PowerShell commands: `Enable-NetAdapter` / `Disable-NetAdapter`
   - Runs in background thread to avoid UI blocking
   - Visual feedback with animated loading indicator

4. **Timer Function:**
   - Spawns dedicated background thread for countdown
   - Updates tooltip every second with formatted time remaining
   - Automatically re-enables adapters when timer expires

5. **Administrator Privileges:**
   - Embedded UAC manifest (`uac_admin=True` in PyInstaller spec)
   - Automatically prompts for elevation on launch
   - Gracefully handles non-admin scenarios with warnings

### File Structure

```
Network Kill Switch/
├── network_kill_switch.py    # Main application code
├── NetworkKillSwitch.spec     # PyInstaller build specification
├── installer.iss              # Inno Setup installer script
├── build_installer.bat        # Automated build script
├── icon.ico                   # Application icon
├── icons/                     # System tray icon assets
│   ├── status_on.ico         # Green (enabled state)
│   ├── status_off.ico        # Red (disabled state)
│   ├── status_loading_*.ico  # Loading animation frames
│   └── status_timer.ico      # Timer active state
├── assets/                    # Documentation assets
│   ├── logofor_readme.png    # README header logo
│   └── *.png                 # Icon source images
├── screenshots/               # Application screenshots
├── setup_task_silent.ps1     # Auto-startup configuration
├── uninstall_task.ps1        # Auto-startup removal
├── check_task_permissions.ps1 # Diagnostic utility
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── BUILD.md                  # Build instructions
├── TROUBLESHOOTING.md        # Extended troubleshooting guide
├── CHANGELOG.md              # Version history
└── LICENSE                   # MIT License
```

## Version History

### Version 2.0.0 (Current)
**Major Update: Rebranded from "Ethernet Toggle" to "Network Kill Switch"**

**New Features:**
- Added WiFi adapter support (in addition to Ethernet)
- Added timer function with 5 preset durations (1m, 2m, 5m, 30m, 1h)
- Live countdown display in tooltip during timer mode
- Animated loading indicator during toggle operations
- Status verification after each toggle operation
- Left-click quick toggle functionality
- Custom icon states (on, off, loading, timer)

**Improvements:**
- Complete rebrand to "Network Kill Switch"
- Enhanced multi-adapter support
- Better error handling and user feedback
- Optimized PowerShell execution for faster response
- ARM64 Windows compatibility via x64 emulation

**Bug Fixes:**
- Fixed icon path resolution in compiled EXE
- Fixed PowerShell subprocess execution in frozen executables
- Fixed admin privilege detection and warnings

### Version 1.0.0 (Legacy)
- Initial release as "Ethernet Toggle"
- Basic Ethernet adapter on/off functionality
- System tray integration
- Simple green/red status indicators

For detailed change history, see [CHANGELOG.md](CHANGELOG.md).

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can use, modify, and distribute this software freely. No warranty is provided.

## Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs
1. Check if the issue already exists in [Issues](https://github.com/chilidogsonic/network-kill-switch/issues)
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your Windows version and system specs

### Suggesting Features
1. Open an issue with the "enhancement" label
2. Describe the feature and its use case
3. Explain why it would be valuable

### Submitting Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes with clear commit messages
4. Test thoroughly on Windows 10 and 11
5. Submit a pull request with a detailed description

### Development Guidelines
- Follow existing code style and conventions
- Comment complex logic
- Test with both Python script and compiled EXE
- Verify admin and non-admin scenarios
- Update documentation for user-facing changes

## Acknowledgments

- **[pystray](https://github.com/moses-palmer/pystray)** - Excellent system tray library
- **[Pillow](https://python-pillow.org/)** - Powerful image processing
- **Windows PowerShell Team** - Network adapter cmdlets
- **Community Contributors** - Bug reports and feature suggestions
- <a href="https://www.flaticon.com/free-icons/no-internet" title="no internet icons">No internet icons created by Yudhi Restu - Flaticon</a>

## Support & Community

- **Issues & Bugs:** [GitHub Issues](https://github.com/chilidogsonic/network-kill-switch/issues)
- **Discussions:** [GitHub Discussions](https://github.com/chilidogsonic/network-kill-switch/discussions)
- **Latest Release:** [Releases Page](https://github.com/chilidogsonic/network-kill-switch/releases)

## Star This Project!

If you find Network Kill Switch useful, please consider:
- Starring this repository
- Reporting bugs or suggesting features
- Sharing with others who might benefit
- Providing feedback

Your support helps improve the project for everyone!

---

<p align="center">
  Made for the Windows community
</p>
<p align="center">
  <sub>Network Kill Switch v2.0.0 | Windows 10/11</sub>
</p>
