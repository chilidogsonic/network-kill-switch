# Ethernet Toggle

A lightweight Windows system tray application that allows you to quickly toggle your Ethernet adapter on/off with a single click.

![Windows](https://img.shields.io/badge/Windows-10%2F11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

## ✨ Features

- 🖥️ **System Tray Integration** - Lives quietly in your Windows system tray
- 🔴🟢 **Visual Status Indicator** - Green = enabled, Red = disabled
- ⚡ **One-Click Toggle** - Right-click to enable/disable your Ethernet adapter
- 🔍 **Auto-Detection** - Automatically finds your Ethernet adapter
- 🚀 **Auto-Startup** - Optional "Start with Windows" during installation
- 📦 **Standalone Installer** - No Python installation required
- 💾 **Lightweight** - Minimal resource usage (~20-30 MB installed)

## 📥 Download

**[Download Latest Release](https://github.com/yourusername/ethernet-toggle/releases/latest)**

Download `EthernetToggle-Setup.exe` from the latest release.

## 🚀 Installation

### For End Users

1. **Download** `EthernetToggle-Setup.exe` from the [Releases](https://github.com/yourusername/ethernet-toggle/releases) page
2. **Run the installer** (requires administrator privileges)
3. **Follow the installation wizard:**
   - Choose installation directory
   - ✅ Check "Start with Windows" to enable automatic startup (recommended)
   - Click Install
4. **Done!** The app will appear in your system tray

**No Python installation required!** The installer includes everything you need.

### Uninstallation

1. Open **Windows Settings** → **Apps** → **Installed apps**
2. Find **"Ethernet Toggle"**
3. Click **Uninstall**

The uninstaller will automatically remove the app and auto-startup configuration.

## 🎯 Usage

1. **Look for the icon** in your system tray (notification area)
   - 🟢 Green circle = Ethernet enabled
   - 🔴 Red circle = Ethernet disabled

2. **Right-click the icon** to see the menu:
   - **Toggle Ethernet (On/Off)** - Click to enable/disable your adapter
   - **Quit** - Close the application

That's it! Simple and straightforward.

## 🛠️ For Developers

### Requirements

- Windows 10/11
- Python 3.7 or higher
- Administrator privileges (required to toggle network adapters)

### Development Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application with administrator privileges:
```bash
# Right-click Command Prompt or PowerShell and select "Run as Administrator"
python ethernet_toggle.py
```

### Easy Startup (Development)

Use the provided batch file to start the application:

1. Right-click `run_ethernet_toggle.bat`
2. Select "Run as administrator"

The app will appear in your system tray.

### Automatic Startup (Development)

If you're running from source and want automatic startup:

1. Right-click `setup_startup.bat` and select "Run as administrator"
2. The script will create a scheduled task for auto-startup

To remove: Run `remove_startup.bat` as administrator.

**Note:** If you used the installer, auto-startup was already configured during installation.

## 🔧 Building from Source

Want to build your own installer? See [BUILD.md](BUILD.md) for detailed instructions.

### Quick Build

```bash
# Install dependencies
pip install -r requirements.txt

# Build the installer
build_installer.bat
```

This creates `Output\EthernetToggle-Setup.exe` that you can distribute.

### Prerequisites

- Python 3.7+
- [Inno Setup 6](https://jrsoftware.org/isinfo.php) (for building installer)
- PyInstaller (auto-installed by build script)

## ❓ Troubleshooting

<details>
<summary><b>"Could not find Ethernet adapter" error</b></summary>

- The app looks for adapters with "Ethernet" in the name
- Check your adapter name in Device Manager (Control Panel → Network Adapters)
- You may need to modify the adapter detection logic for non-standard names
</details>

<details>
<summary><b>Toggle doesn't work</b></summary>

- Ensure you're running as Administrator
- Verify your adapter name in Device Manager
- Check Windows Event Viewer for errors
</details>

<details>
<summary><b>Auto-startup not working</b></summary>

- Open Task Scheduler and look for "EthernetToggleApp"
- Verify the task is enabled and configured correctly
- Check Task Scheduler History for error messages
</details>

<details>
<summary><b>Icon doesn't appear in system tray</b></summary>

- Check if the app is running in Task Manager
- Look in the overflow area (hidden icons) in system tray
- Try restarting the application
</details>

## 📋 Technical Details

- **Language:** Python 3.7+
- **UI Framework:** pystray (system tray integration)
- **Image Processing:** Pillow (for icon generation)
- **Network Control:** Windows PowerShell (`Enable-NetAdapter` / `Disable-NetAdapter`)
- **Packaging:** PyInstaller (standalone executable)
- **Installer:** Inno Setup (Windows installer creation)
- **Size:** ~20-30 MB (includes Python runtime)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## ⭐ Support

If you find this tool useful, please consider giving it a star on GitHub!
