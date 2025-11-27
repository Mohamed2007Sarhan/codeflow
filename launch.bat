@echo off
REM Launcher script for Code Analysis and Debugging Visualizer

echo Starting Code Analysis and Debugging Visualizer...
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Run the main application
python main.py

REM Deactivate virtual environment
call deactivate

echo.
echo Application closed.
pause