"""
Test script to verify the enhanced debugging functionality with project support
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_project_debugging():
    """Test the enhanced debugging engine with project support"""
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    x = 10
    y = 20
    result = fibonacci(x)
    print(f"Fibonacci of {x} is {result}")
    
    # This will cause an error for demonstration
    z = 1 / 0  # Division by zero error
    
    numbers = [1, 2, 3, 4, 5]
    total = 0
    for num in numbers:
        total += num
    
    if total > 10:
        print("Total is greater than 10")
    else:
        print("Total is 10 or less")

if __name__ == "__main__":
    main()
"""
    
    try:
        from analyzer.debug_engine import DebuggingEngine
        engine = DebuggingEngine(sample_code, "test_module.py")
        
        print("Testing Enhanced Debugging Engine with Project Support...")
        print("=" * 60)
        
        if engine.parse():
            print("✓ Code parsed successfully")
            engine.initialize_execution_steps()
            print(f"✓ Initialized {len(engine.execution_steps)} execution steps")
            print(f"✓ File name tracked: {engine.filename}")
            
            # Test execution flow tracking
            print("\nTesting execution flow tracking:")
            for i in range(min(5, len(engine.execution_steps))):  # Test first 5 steps
                if engine.step_forward():
                    current_step = engine.execution_steps[engine.current_step]
                    line_state = engine.get_line_state(current_step['line'])
                    execution_flow = engine.get_execution_flow()
                    print(f"  Step {i+1}: Line {current_step['line']} [{current_step['filename']}] - {line_state['status']}")
                    print(f"    Execution flow length: {len(execution_flow)}")
                    
                    # Check for errors
                    if engine.has_error():
                        error_info = engine.get_error_info()
                        print(f"  ERROR in {error_info['filename']} at line {error_info['line']}: {error_info['message']}")
                        break
                else:
                    print(f"  Failed to execute step {i+1}")
                    break
                    
            # Test reset functionality
            print(f"\nTesting reset functionality:")
            engine.reset_execution()
            print(f"✓ Execution reset - Flow length: {len(engine.get_execution_flow())}")
            print(f"✓ Current step: {engine.current_step}")
            
            # Test error handling
            print(f"\nError status: {'Yes' if engine.has_error() else 'No'}")
            if engine.has_error():
                error_info = engine.get_error_info()
                print(f"Error file: {error_info['filename']}")
                print(f"Error line: {error_info['line']}")
                print(f"Error message: {error_info['message']}")
                
        else:
            print("✗ Failed to parse code")
            error_info = engine.get_error_info()
            if error_info['has_error']:
                print(f"Syntax Error in {error_info['filename']} at line {error_info['line']}: {error_info['message']}")
                
    except Exception as e:
        print(f"✗ Error testing debugging engine: {e}")

def test_flow_graph_generation():
    """Test flow graph generation"""
    print("\n\nTesting Flow Graph Generation...")
    print("=" * 60)
    
    try:
        from visualization.flow_graph import FlowGraphVisualizer
        
        # Sample execution steps
        execution_steps = [
            {'line': 1, 'type': 'FunctionDef', 'description': 'Define fibonacci function', 'filename': 'main.py'},
            {'line': 2, 'type': 'If', 'description': 'Check if n <= 1', 'filename': 'main.py'},
            {'line': 3, 'type': 'Return', 'description': 'Return n', 'filename': 'main.py'},
            {'line': 5, 'type': 'Return', 'description': 'Recursive call', 'filename': 'main.py'},
            {'line': 8, 'type': 'Assign', 'description': 'Assign x = 10', 'filename': 'main.py'},
            {'line': 9, 'type': 'Assign', 'description': 'Assign result = fibonacci(x)', 'filename': 'main.py'},
            {'line': 10, 'type': 'Print', 'description': 'Print result', 'filename': 'main.py'}
        ]
        
        # Create and generate flow graph
        visualizer = FlowGraphVisualizer()
        graph = visualizer.generate_flow_graph(execution_steps)
        
        # Get graph data
        graph_data = visualizer.get_graph_data()
        
        print("✓ Flow graph generated successfully")
        print(f"✓ Nodes created: {len(graph_data['nodes'])}")
        print(f"✓ Edges created: {len(graph_data['edges'])}")
        
        # Show sample nodes and edges
        print("\nSample nodes:")
        for node in graph_data['nodes'][:3]:
            print(f"  {node['id']}: {node['label']}")
            
        print("\nSample edges:")
        for edge in graph_data['edges'][:3]:
            print(f"  {edge['source']} -> {edge['target']}: {edge['label']}")
            
    except Exception as e:
        print(f"✗ Error testing flow graph generation: {e}")

if __name__ == "__main__":
    test_project_debugging()
    test_flow_graph_generation()
    print("\n" + "=" * 60)
    print("All enhanced functionality tests completed!")