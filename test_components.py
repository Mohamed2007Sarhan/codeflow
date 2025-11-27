"""
Test script to verify the application components
"""

import sys
import os
import tempfile
import sqlite3
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from analyzer.ast_analyzer import ASTAnalyzer
        print("✓ ASTAnalyzer imported successfully")
    except Exception as e:
        print(f"✗ Failed to import ASTAnalyzer: {e}")
        
    try:
        from analyzer.debug_engine import DebuggingEngine
        print("✓ DebuggingEngine imported successfully")
    except Exception as e:
        print(f"✗ Failed to import DebuggingEngine: {e}")
        
    try:
        from db.history_db import HistoryDatabase
        print("✓ HistoryDatabase imported successfully")
    except Exception as e:
        print(f"✗ Failed to import HistoryDatabase: {e}")
        
    try:
        from visualization.flow_graph import FlowGraphVisualizer
        print("✓ FlowGraphVisualizer imported successfully")
    except Exception as e:
        print(f"✗ Failed to import FlowGraphVisualizer: {e}")
        
    try:
        from utils.export_utils import export_to_json, export_to_html
        print("✓ Export utilities imported successfully")
    except Exception as e:
        print(f"✗ Failed to import export utilities: {e}")

def test_analyzer():
    """Test the AST analyzer with sample code"""
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

x = 10
result = fibonacci(x)
print(result)
"""
    
    try:
        from analyzer.ast_analyzer import ASTAnalyzer
        analyzer = ASTAnalyzer(sample_code)
        if analyzer.analyze():
            results = analyzer.get_results()
            print("✓ AST analysis completed successfully")
            print(f"  Variables found: {len(results['variables'])}")
            print(f"  Functions found: {len(results['functions'])}")
            print(f"  Classes found: {len(results['classes'])}")
            print(f"  Conditionals found: {len(results['conditionals'])}")
            print(f"  Loops found: {len(results['loops'])}")
        else:
            print("✗ AST analysis failed")
    except Exception as e:
        print(f"✗ Error in AST analysis: {e}")

def test_database():
    """Test the database functionality"""
    try:
        # Create a temporary database file for testing
        import tempfile
        import os
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        from db.history_db import HistoryDatabase
        db = HistoryDatabase(temp_db.name)
        
        session_id = db.save_session(
            "test.py",
            "print('Hello')",
            {"variables": []},
            [{"line": 1, "type": "print"}],
            {"message": "Hello"},
            {"nodes": []}
        )
        print(f"✓ Database test successful, session ID: {session_id}")
        
        # Clean up
        os.unlink(temp_db.name)
    except Exception as e:
        print(f"✗ Database test failed: {e}")

if __name__ == "__main__":
    print("Testing application components...")
    print("=" * 40)
    test_imports()
    print()
    test_analyzer()
    print()
    test_database()
    print("=" * 40)
    print("Testing complete!")