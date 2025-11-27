#!/usr/bin/env python3
"""
Code Analysis and Debugging Visualizer
A desktop GUI application for code analysis, execution visualization, and interactive debugging.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Set application name and icon
    app.setApplicationName("CodeFlow Debugger")
    app.setApplicationDisplayName("CodeFlow Debugger")
    app.setOrganizationName("CodeFlow")
    app.setOrganizationDomain("codeflow.debugger")
    
    # Set window icon if images.png exists
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    
    # Also set icon for the main window
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()