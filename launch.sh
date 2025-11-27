#!/bin/bash
# Launcher script for Code Analysis and Debugging Visualizer

echo "Starting Code Analysis and Debugging Visualizer..."
echo

# Activate virtual environment
source venv/bin/activate

# Run the main application
python main.py

# Deactivate virtual environment
deactivate

echo
echo "Application closed."