
# Multi-Language Demo for Code Analysis and Debugging Visualizer

This demo showcases the multi-language capabilities of the enhanced debugging visualizer.

## Languages Supported

1. **Python** (python_demo.py) - Native support with full AST analysis
2. **C++** (cpp_demo.cpp) - Simulated debugging with compiler support
3. **Java** (java_demo.java) - Simulated debugging with compiler support
4. **JavaScript** (js_demo.js) - Simulated debugging

## Features Demonstrated

- Multi-language project loading
- Language-specific file filtering
- Compiler path configuration for non-Python languages
- Simulated debugging for compiled languages
- Cross-language navigation
- Execution flow visualization
- Error detection and highlighting

## How to Use with the Debugger

1. Open the application
2. Select programming language from the language selection dialog
3. For non-Python languages, optionally specify compiler path
4. Open individual files or entire project folders
5. Run analysis and step through execution
6. Observe:
   - Green lines: Successfully executed
   - Red lines: Errors detected
   - Blue line: Currently executing
   - Timeline indicators: ✓ (success), ✗ (error), ○ (pending), ● (current)
7. Switch between files using the file selector
8. View execution flow graph in the Flow Graph tab

## Language-Specific Notes

### Python
- Full AST-based analysis
- Real-time variable tracking
- Complete debugging support

### C++
- Simulated execution steps
- Compiler path: g++ (GCC) or clang++
- Syntax validation

### Java
- Simulated execution steps
- Compiler path: javac
- Syntax validation

### JavaScript
- Simulated execution steps
- No compiler needed for basic debugging
- Syntax validation
