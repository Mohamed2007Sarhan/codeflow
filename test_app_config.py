"""
Test script to verify the application icon and name configuration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_application_configuration():
    """Test the application configuration"""
    print("Testing Application Configuration...")
    print("=" * 40)
    
    # Check if images.png exists
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images.png")
    if os.path.exists(icon_path):
        print("✓ Application icon file found")
        print(f"  Icon path: {icon_path}")
        # Check file size
        file_size = os.path.getsize(icon_path)
        print(f"  Icon file size: {file_size} bytes")
    else:
        print("✗ Application icon file not found")
        
    # Check main application configuration
    try:
        from main import main
        print("✓ Main application module imported successfully")
    except Exception as e:
        print(f"✗ Error importing main application: {e}")
        
    # Check main window configuration
    try:
        from ui.main_window import MainWindow
        print("✓ Main window module imported successfully")
    except Exception as e:
        print(f"✗ Error importing main window: {e}")
        
    # Print application information
    print("\nApplication Information:")
    print("  Name: CodeFlow Debugger")
    print("  Organization: CodeFlow")
    print("  Window Title: CodeFlow Debugger")
    
    # Check if we can read the icon file
    if os.path.exists(icon_path):
        try:
            # Try to open and read a small portion of the file to verify it's valid
            with open(icon_path, 'rb') as f:
                header = f.read(8)
                print(f"✓ Icon file header: {header.hex()}")
        except Exception as e:
            print(f"✗ Error reading icon file: {e}")

if __name__ == "__main__":
    test_application_configuration()
    print("\n" + "=" * 40)
    print("Application configuration test completed!")