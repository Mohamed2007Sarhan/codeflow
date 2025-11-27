# Code Analysis and Debugging Visualizer

A desktop GUI application for code analysis, execution visualization, and interactive debugging.

The Folder lib in venv not added content with me for send to you whatsapp : +201040922321

## Features

- File upload and language selection (Python support)
- Code structure analysis (AST parsing)
- Interactive debugging with step-by-step execution
- Visual execution flow graph
- SQL-based history system
- Dark theme UI with professional design
- Export to JSON/HTML formats

## Components

1. **UI Layer** - PyQt5 based graphical interface
2. **Analyzer** - AST-based code analysis engine
3. **Debugger** - Interactive execution engine
4. **Database** - SQLite-based session storage
5. **Visualization** - Flow graph rendering
6. **Utilities** - Export and helper functions

## Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

You can run the application in several ways:

1. **Direct execution:**
   ```
   python main.py
   ```

2. **Using the launcher script (Windows):**
   ```
   launch.bat
   ```

3. **Using the launcher script (macOS/Linux):**
   ```
   ./launch.sh
   ```

### Using the Application

1. **File Operations:**
   - Click "File" → "Open" or use the toolbar "Open" button
   - Select a Python file to analyze
   - The application will automatically parse and analyze the code

2. **Analysis Process:**
   - After loading a file, click "Run" or the toolbar "Run" button
   - A progress dialog will show the analysis steps
   - Once complete, the right panels will show structured code information

3. **Debugging:**
   - After analysis, select operations to debug
   - Use the control buttons at the bottom to step through execution
   - View variable states and execution timeline

4. **History:**
   - Previous sessions are stored in the left sidebar
   - Click on any session to load it

5. **Export:**
   - File → Export → JSON/HTML to export session data

## Project Structure

```
├── main.py              # Application entry point
├── requirements.txt     # Dependencies
├── launch.bat           # Windows launcher script
├── launch.sh            # macOS/Linux launcher script
├── README.md            # This file
├── test_sample.py       # Sample Python file for testing
├── test_components.py   # Component testing script
├── ui/
│   └── main_window.py   # Main GUI window
├── analyzer/
│   ├── ast_analyzer.py  # AST-based code analysis
│   └── debug_engine.py  # Debugging engine
├── db/
│   └── history_db.py    # Database interface
├── visualization/
│   └── flow_graph.py    # Flow graph visualization
└── utils/
    └── export_utils.py  # Export utilities
```

## Development Roadmap

### Phase 1 - Complete ✓
- GUI skeleton with dark theme
- File upload and progress screen
- AST extraction and analysis

### Phase 2 - Complete ✓
- GUI panels for variables, functions, classes, conditionals
- Operation selection mode

### Phase 3 - In Progress
- Execution engine with timeline
- Variable live updates during debugging

### Phase 4 - Pending
- Flow graph visualization
- Node interactions and branch tracking

### Phase 5 - Pending
- Manual editing system
- Re-run logic for edited steps

### Phase 6 - Pending
- History database integration
- Session loading system

### Phase 7 - Pending
- Advanced features (variable timeline graph, function execution map)
- Export system (JSON, HTML)
- Multi-file support

## Requirements

- Python 3.6+
- PyQt5
- astor
- networkx
- matplotlib
- sqlalchemy

## License


This project is licensed under the MIT License - see the LICENSE file for details.
