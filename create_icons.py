"""
Script to convert PNG images to ICO format for system tray icons
"""
from PIL import Image
import os

def create_ico_from_pngs(png_files, output_ico):
    """Create a multi-resolution ICO file from PNG files"""
    images = []
    for png_file in png_files:
        if os.path.exists(png_file):
            img = Image.open(png_file)
            images.append(img)
        else:
            print(f"Warning: {png_file} not found")

    if images:
        # Save as ICO with multiple sizes
        images[0].save(output_ico, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
        print(f"Created: {output_ico}")
        return True
    return False

# Create icons directory if it doesn't exist
os.makedirs('icons', exist_ok=True)

# Create icon for "On" state (green)
on_files = [
    'assets/statusOn_16.png',
    'assets/statusOn_32.png',
    'assets/statusOn_48.png'
]
create_ico_from_pngs(on_files, 'icons/status_on.ico')

# Create icon for "Off" state (red)
off_files = [
    'assets/statusOff_16.png',
    'assets/statusOff_32.png',
    'assets/statusOff_48.png'
]
create_ico_from_pngs(off_files, 'icons/status_off.ico')

print("\nIcon conversion complete!")
print("Generated icons:")
print("  - icons/status_on.ico (green - enabled)")
print("  - icons/status_off.ico (red - disabled)")
