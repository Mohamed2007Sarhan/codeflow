"""
Utility functions for the Code Analysis and Debugging Visualizer
"""

import json
import os

def export_to_json(data, filename):
    """Export data to JSON format"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return False

def export_to_html(data, filename):
    """Export data to HTML format"""
    try:
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Code Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1, h2 {{ color: #333; }}
        .panel {{ margin-bottom: 30px; }}
        .panel h2 {{ border-bottom: 2px solid #4b6eaf; padding-bottom: 10px; }}
        .code-block {{ background-color: #1e1e1e; color: #ffffff; padding: 15px; border-radius: 5px; font-family: 'Consolas', monospace; overflow-x: auto; }}
        .data-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        .data-table th, .data-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .data-table th {{ background-color: #4b6eaf; color: white; }}
        .data-table tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Code Analysis Report</h1>
        
        <div class="panel">
            <h2>Code</h2>
            <div class="code-block">
                {data.get('code', '').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')}
            </div>
        </div>
        
        <div class="panel">
            <h2>Variables</h2>
            <table class="data-table">
                <tr><th>Name</th><th>Value</th><th>Line</th></tr>
        """
        
        # Add variables data
        for var in data.get('variables', []):
            html_content += f"<tr><td>{var.get('name', '')}</td><td>{var.get('value', '')}</td><td>{var.get('line', '')}</td></tr>"
            
        html_content += """
            </table>
        </div>
        
        <div class="panel">
            <h2>Functions</h2>
            <table class="data-table">
                <tr><th>Name</th><th>Parameters</th><th>Line</th></tr>
        """
        
        # Add functions data
        for func in data.get('functions', []):
            params = ", ".join(func.get('params', []))
            html_content += f"<tr><td>{func.get('name', '')}</td><td>{params}</td><td>{func.get('line', '')}</td></tr>"
            
        html_content += """
            </table>
        </div>
        
        <div class="panel">
            <h2>Classes</h2>
            <table class="data-table">
                <tr><th>Name</th><th>Methods</th><th>Line</th></tr>
        """
        
        # Add classes data
        for cls in data.get('classes', []):
            methods = ", ".join(cls.get('methods', []))
            html_content += f"<tr><td>{cls.get('name', '')}</td><td>{methods}</td><td>{cls.get('line', '')}</td></tr>"
            
        html_content += """
            </table>
        </div>
        
        <div class="panel">
            <h2>Execution Steps</h2>
            <table class="data-table">
                <tr><th>Step</th><th>Description</th><th>Line</th></tr>
        """
        
        # Add execution steps data
        for i, step in enumerate(data.get('execution_steps', [])):
            html_content += f"<tr><td>{i+1}</td><td>{step.get('description', '')}</td><td>{step.get('line', '')}</td></tr>"
            
        html_content += """
            </table>
        </div>
    </div>
</body>
</html>
        """
        
        with open(filename, 'w') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"Error exporting to HTML: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_data = {
        "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return fibonacci(n-1) + fibonacci(n-2)",
        "variables": [
            {"name": "x", "value": "10", "line": 8},
            {"name": "result", "value": "fibonacci(x)", "line": 10}
        ],
        "functions": [
            {"name": "fibonacci", "params": ["n"], "line": 1},
            {"name": "main", "params": [], "line": 6}
        ],
        "classes": [],
        "execution_steps": [
            {"line": 1, "type": "FunctionDef", "description": "Define fibonacci function"},
            {"line": 2, "type": "If", "description": "Check if n <= 1"},
            {"line": 8, "type": "Assign", "description": "Assign x = 10"},
            {"line": 10, "type": "Assign", "description": "Assign result = fibonacci(x)"}
        ]
    }
    
    # Test exports
    export_to_json(sample_data, "test_export.json")
    export_to_html(sample_data, "test_export.html")
    print("Export tests completed")