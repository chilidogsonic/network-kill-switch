"""
Lightweight System Tray Application for Toggling Ethernet Adapter
"""
import subprocess
import pystray
from PIL import Image
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
        self.timer_thread = None
        self.timer_cancel = False

        # Try to load custom icons
        self.icon_on = self.load_icon('icons/status_on.ico')
        self.icon_off = self.load_icon('icons/status_off.ico')

    def load_icon(self, path):
        """Load icon from file if it exists"""
        try:
            if os.path.exists(path):
                return Image.open(path)
        except Exception as e:
            if not self.silent_mode:
                print(f"Could not load icon {path}: {e}")
        return None

    def create_icon_image(self, enabled=True):
        """Create or load icon image based on state"""
        # Use custom icons if available
        if enabled and self.icon_on:
            return self.icon_on
        elif not enabled and self.icon_off:
            return self.icon_off

        # Fallback to generated icon
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(image)

        # Draw a circle
        color = (0, 255, 0, 255) if enabled else (255, 0, 0, 255)
        draw.ellipse([8, 8, 56, 56], fill=color, outline=(255, 255, 255, 255))

        # Draw ethernet symbol (simplified)
        draw.rectangle([24, 20, 40, 24], fill=(255, 255, 255, 255))
        draw.rectangle([28, 24, 36, 44], fill=(255, 255, 255, 255))

        return image

    def find_ethernet_adapter(self):
        """Find the first Ethernet adapter"""
        try:
            # PowerShell command to get network adapters
            cmd = 'powershell -Command "Get-NetAdapter | Where-Object {$_.InterfaceDescription -like \'*Ethernet*\' -or $_.Name -like \'*Ethernet*\'} | Select-Object -First 1 | ConvertTo-Json"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=10)

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
        """Check if the adapter is currently enabled with verification"""
        if not self.adapter_name:
            return False

        try:
            cmd = f'powershell -Command "Get-NetAdapter -Name \'{self.adapter_name}\' | Select-Object Status"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=10)
            return 'Up' in result.stdout
        except:
            return False

    def verify_status_change(self, expected_status, max_attempts=10, delay=0.5):
        """Verify that the adapter status has changed to expected state"""
        for attempt in range(max_attempts):
            time.sleep(delay)
            current_status = self.get_adapter_status()
            if current_status == expected_status:
                return True
        return False

    def toggle_adapter(self, enable=None):
        """Toggle the Ethernet adapter on/off, or set to specific state"""
        if not self.adapter_name:
            return

        # Determine target state
        if enable is None:
            target_enabled = not self.is_enabled
        else:
            target_enabled = enable

        try:
            if target_enabled:
                # Enable adapter
                cmd = f'powershell -Command "Enable-NetAdapter -Name \'{self.adapter_name}\' -Confirm:$false"'
                subprocess.run(cmd, shell=True, check=True, timeout=30)
            else:
                # Disable adapter
                cmd = f'powershell -Command "Disable-NetAdapter -Name \'{self.adapter_name}\' -Confirm:$false"'
                subprocess.run(cmd, shell=True, check=True, timeout=30)

            # Verify the status change
            if self.verify_status_change(target_enabled):
                self.is_enabled = target_enabled
            else:
                # Force check current status if verification failed
                self.is_enabled = self.get_adapter_status()

            # Update icon to reflect actual state
            self.update_icon()

        except subprocess.CalledProcessError as e:
            if not self.silent_mode:
                print(f"Error toggling adapter: {e}")
            # Still update to actual state
            self.is_enabled = self.get_adapter_status()
            self.update_icon()

    def update_icon(self):
        """Update the tray icon based on adapter state"""
        if self.icon:
            self.icon.icon = self.create_icon_image(self.is_enabled)
            status = "Enabled" if self.is_enabled else "Disabled"
            self.icon.title = f"Ethernet: {status}"

    def cancel_timer(self):
        """Cancel any running timer"""
        self.timer_cancel = True
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
        self.timer_cancel = False

    def start_timer(self, seconds):
        """Disable adapter for a specified duration, then re-enable"""
        def timer_worker():
            # Disable the adapter
            self.toggle_adapter(enable=False)

            # Wait for the specified duration (check for cancellation)
            start_time = time.time()
            while not self.timer_cancel and (time.time() - start_time) < seconds:
                time.sleep(0.5)

            # Re-enable the adapter if timer wasn't cancelled
            if not self.timer_cancel:
                self.toggle_adapter(enable=True)

        # Cancel any existing timer
        self.cancel_timer()

        # Start new timer thread
        self.timer_thread = threading.Thread(target=timer_worker, daemon=True)
        self.timer_thread.start()

    def on_toggle_click(self, icon, item):
        """Handle toggle menu item click"""
        self.toggle_adapter()

    def on_left_click(self, icon, item=None):
        """Handle left-click on icon - quick toggle"""
        self.toggle_adapter()

    def on_timer_click(self, icon, item):
        """Handle timer menu item click"""
        # Extract duration from menu item text
        text = str(item)
        if "1 minute" in text:
            self.start_timer(60)
        elif "2 minutes" in text:
            self.start_timer(120)
        elif "5 minutes" in text:
            self.start_timer(300)
        elif "30 minutes" in text:
            self.start_timer(1800)
        elif "1 hour" in text:
            self.start_timer(3600)

    def on_cancel_timer(self, icon, item):
        """Handle cancel timer menu item"""
        self.cancel_timer()
        self.toggle_adapter(enable=True)  # Ensure adapter is back on

    def on_quit(self, icon, item):
        """Handle quit menu item click"""
        self.cancel_timer()
        icon.stop()

    def setup_icon(self):
        """Setup the system tray icon"""
        # Initial detection
        if not self.find_ethernet_adapter():
            if not self.silent_mode:
                print("Warning: Could not find Ethernet adapter")
            self.adapter_name = "Ethernet"  # Fallback name

        self.detecting_adapter = False

        # Create menu with timer options
        menu = pystray.Menu(
            pystray.MenuItem(
                lambda text: f"Toggle Ethernet ({'On' if not self.is_enabled else 'Off'})",
                self.on_toggle_click,
                default=True  # Left-click action
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Disable for...",
                pystray.Menu(
                    pystray.MenuItem("1 minute", self.on_timer_click),
                    pystray.MenuItem("2 minutes", self.on_timer_click),
                    pystray.MenuItem("5 minutes", self.on_timer_click),
                    pystray.MenuItem("30 minutes", self.on_timer_click),
                    pystray.MenuItem("1 hour", self.on_timer_click),
                    pystray.Menu.SEPARATOR,
                    pystray.MenuItem("Cancel Timer", self.on_cancel_timer)
                )
            ),
            pystray.Menu.SEPARATOR,
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
