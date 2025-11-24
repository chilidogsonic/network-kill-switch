"""
Lightweight System Tray Application for Toggling Ethernet Adapter
"""
import subprocess
import pystray
from PIL import Image, ImageDraw
import threading
import time
import sys
import os


class EthernetToggle:
    def __init__(self, silent_mode=False):
        self.adapter_name = None
        self.is_enabled = False
        self.icon = None
        self.detecting_adapter = True
        self.silent_mode = silent_mode

    def find_ethernet_adapter(self):
        """Find the first Ethernet adapter"""
        try:
            # PowerShell command to get network adapters
            cmd = 'powershell -Command "Get-NetAdapter | Where-Object {$_.InterfaceDescription -like \'*Ethernet*\' -or $_.Name -like \'*Ethernet*\'} | Select-Object -First 1 | ConvertTo-Json"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

            if result.returncode == 0 and result.stdout.strip():
                import json
                adapter = json.loads(result.stdout)
                self.adapter_name = adapter['Name']
                self.is_enabled = adapter['Status'] == 'Up'
                return True
        except Exception as e:
            if not self.silent_mode:
                print(f"Error finding adapter: {e}")

        return False

    def get_adapter_status(self):
        """Check if the adapter is currently enabled"""
        if not self.adapter_name:
            return False

        try:
            cmd = f'powershell -Command "Get-NetAdapter -Name \'{self.adapter_name}\' | Select-Object Status"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return 'Up' in result.stdout
        except:
            return False

    def toggle_adapter(self):
        """Toggle the Ethernet adapter on/off"""
        if not self.adapter_name:
            return

        try:
            if self.is_enabled:
                # Disable adapter
                cmd = f'powershell -Command "Disable-NetAdapter -Name \'{self.adapter_name}\' -Confirm:$false"'
                subprocess.run(cmd, shell=True, check=True)
                self.is_enabled = False
            else:
                # Enable adapter
                cmd = f'powershell -Command "Enable-NetAdapter -Name \'{self.adapter_name}\' -Confirm:$false"'
                subprocess.run(cmd, shell=True, check=True)
                self.is_enabled = True

            # Update icon
            time.sleep(0.5)  # Wait for adapter state to change
            self.is_enabled = self.get_adapter_status()
            self.update_icon()

        except subprocess.CalledProcessError as e:
            if not self.silent_mode:
                print(f"Error toggling adapter: {e}")

    def create_icon_image(self, enabled=True):
        """Create a simple icon image"""
        # Create a 64x64 image
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw a circle
        color = (0, 255, 0, 255) if enabled else (255, 0, 0, 255)
        draw.ellipse([8, 8, 56, 56], fill=color, outline=(255, 255, 255, 255))

        # Draw ethernet symbol (simplified)
        draw.rectangle([24, 20, 40, 24], fill=(255, 255, 255, 255))
        draw.rectangle([28, 24, 36, 44], fill=(255, 255, 255, 255))

        return image

    def update_icon(self):
        """Update the tray icon based on adapter state"""
        if self.icon:
            self.icon.icon = self.create_icon_image(self.is_enabled)
            status = "Enabled" if self.is_enabled else "Disabled"
            self.icon.title = f"Ethernet: {status}"

    def on_toggle_click(self, icon, item):
        """Handle toggle menu item click"""
        self.toggle_adapter()

    def on_quit(self, icon, item):
        """Handle quit menu item click"""
        icon.stop()

    def setup_icon(self):
        """Setup the system tray icon"""
        # Initial detection
        if not self.find_ethernet_adapter():
            if not self.silent_mode:
                print("Warning: Could not find Ethernet adapter")
            self.adapter_name = "Ethernet"  # Fallback name

        self.detecting_adapter = False

        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem(
                lambda text: f"Toggle Ethernet ({'On' if not self.is_enabled else 'Off'})",
                self.on_toggle_click
            ),
            pystray.MenuItem("Quit", self.on_quit)
        )

        # Create icon
        status = "Enabled" if self.is_enabled else "Disabled"
        self.icon = pystray.Icon(
            "ethernet_toggle",
            self.create_icon_image(self.is_enabled),
            f"Ethernet: {status}",
            menu
        )

        # Run icon
        self.icon.run()


def main():
    """Main entry point"""
    # Check for silent mode flag
    silent_mode = '--silent' in sys.argv or len(sys.argv) == 1 and os.path.basename(sys.executable) == 'pythonw.exe'

    if not silent_mode:
        print("Starting Ethernet Toggle Application...")
        print("Note: This application requires administrator privileges to toggle network adapters.")

    app = EthernetToggle(silent_mode=silent_mode)
    app.setup_icon()


if __name__ == "__main__":
    main()
