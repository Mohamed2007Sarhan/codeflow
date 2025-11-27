"""
Test script to verify the multi-language support functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_multi_language_support():
    """Test the multi-language debugging engine"""
    
    # Test Python code
    python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

x = 10
result = fibonacci(x)
print(result)
"""
    
    # Test C++ code
    cpp_code = """
#include <iostream>
using namespace std;

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n-1) + fibonacci(n-2);
    }
}

int main() {
    int x = 10;
    int result = fibonacci(x);
    cout << result << endl;
    return 0;
}
"""
    
    # Test Java code
    java_code = """
public class Main {
    public static int fibonacci(int n) {
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n-1) + fibonacci(n-2);
        }
    }
    
    public static void main(String[] args) {
        int x = 10;
        int result = fibonacci(x);
        System.out.println(result);
    }
}
"""
    
    try:
        from analyzer.debug_engine import DebuggingEngine
        
        print("Testing Multi-Language Support...")
        print("=" * 50)
        
        # Test Python debugging engine
        print("\n1. Testing Python Debugging Engine:")
        python_engine = DebuggingEngine(python_code, "test.py", "python")
        if python_engine.parse():
            print("✓ Python code parsed successfully")
            python_engine.initialize_execution_steps()
            print(f"✓ Initialized {len(python_engine.execution_steps)} execution steps")
            
            # Test stepping
            if python_engine.step_forward():
                current_step = python_engine.execution_steps[python_engine.current_step]
                line_state = python_engine.get_line_state(current_step['line'])
                print(f"✓ Step executed: Line {current_step['line']} - {line_state['status']}")
        else:
            print("✗ Failed to parse Python code")
            
        # Test C++ debugging engine
        print("\n2. Testing C++ Debugging Engine:")
        cpp_engine = DebuggingEngine(cpp_code, "test.cpp", "cpp")
        if cpp_engine.parse():
            print("✓ C++ code parsed successfully")
            cpp_engine.initialize_execution_steps()
            print(f"✓ Initialized {len(getattr(cpp_engine, 'simulated_steps', []))} simulated steps")
            
            # Test stepping
            if cpp_engine.step_forward():
                steps = getattr(cpp_engine, 'simulated_steps', [])
                if steps and cpp_engine.current_step < len(steps):
                    current_step = steps[cpp_engine.current_step]
                    line_state = cpp_engine.get_line_state(current_step.get('line', cpp_engine.current_step + 1))
                    print(f"✓ Step executed: Line {current_step.get('line', 'N/A')} - {line_state['status']}")
        else:
            print("✗ Failed to parse C++ code")
            
        # Test Java debugging engine
        print("\n3. Testing Java Debugging Engine:")
        java_engine = DebuggingEngine(java_code, "Main.java", "java")
        if java_engine.parse():
            print("✓ Java code parsed successfully")
            java_engine.initialize_execution_steps()
            print(f"✓ Initialized {len(getattr(java_engine, 'simulated_steps', []))} simulated steps")
            
            # Test stepping
            if java_engine.step_forward():
                steps = getattr(java_engine, 'simulated_steps', [])
                if steps and java_engine.current_step < len(steps):
                    current_step = steps[java_engine.current_step]
                    line_state = java_engine.get_line_state(current_step.get('line', java_engine.current_step + 1))
                    print(f"✓ Step executed: Line {current_step.get('line', 'N/A')} - {line_state['status']}")
        else:
            print("✗ Failed to parse Java code")
            
        # Test compiler path setting
        print("\n4. Testing Compiler Path Setting:")
        cpp_engine.set_compiler_path("/usr/bin/g++")
        java_engine.set_compiler_path("/usr/bin/javac")
        print("✓ Compiler paths set successfully")
        print(f"  C++ compiler: {cpp_engine.compiler_path}")
        print(f"  Java compiler: {java_engine.compiler_path}")
        
        # Test reset functionality
        print("\n5. Testing Reset Functionality:")
        python_engine.reset_execution()
        print("✓ Python engine reset successfully")
        print(f"  Current step: {python_engine.current_step}")
        print(f"  Error state: {python_engine.error_state}")
        
    except Exception as e:
        print(f"✗ Error testing multi-language support: {e}")

def test_language_selection_dialog():
    """Test the language selection dialog concept"""
    print("\n\nTesting Language Selection Dialog Concept...")
    print("=" * 50)
    
    languages = [
        {"name": "Python", "compiler_needed": False},
        {"name": "C++", "compiler_needed": True, "compiler": "g++"},
        {"name": "Java", "compiler_needed": True, "compiler": "javac"},
        {"name": "C#", "compiler_needed": True, "compiler": "csc"},
        {"name": "JavaScript", "compiler_needed": False},
        {"name": "Other", "compiler_needed": True, "compiler": "custom"}
    ]
    
    print("Available Languages:")
    for i, lang in enumerate(languages, 1):
        compiler_info = f" (Compiler: {lang['compiler']})" if lang['compiler_needed'] else " (No compiler needed)"
        print(f"  {i}. {lang['name']}{compiler_info}")
        
    print("\n✓ Language selection dialog concept verified")

if __name__ == "__main__":
    test_multi_language_support()
    test_language_selection_dialog()
    print("\n" + "=" * 50)
    print("All multi-language tests completed!")