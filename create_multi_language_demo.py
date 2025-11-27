"""
Comprehensive demonstration of the enhanced multi-language Code Analysis and Debugging Visualizer
This script creates sample files for different programming languages
"""

import os

# Create a multi-language demo directory
demo_dir = "multi_language_demo"
os.makedirs(demo_dir, exist_ok=True)

# Create Python demo
python_demo = '''
"""
Python Demo for Multi-Language Debugger
Demonstrates recursive functions, classes, and error handling
"""

class Calculator:
    """A simple calculator class"""
    
    def __init__(self, precision=2):
        self.precision = precision
        self.history = []
        
    def fibonacci(self, n):
        """Calculate fibonacci number recursively"""
        if n <= 1:
            return n
        else:
            return self.fibonacci(n-1) + self.fibonacci(n-2)
            
    def factorial(self, n):
        """Calculate factorial"""
        if n <= 1:
            return 1
        else:
            return n * self.factorial(n-1)

def main():
    """Main function"""
    calc = Calculator()
    
    # Test fibonacci
    fib_result = calc.fibonacci(10)
    print(f"Fibonacci of 10: {fib_result}")
    
    # Test factorial
    fact_result = calc.factorial(5)
    print(f"Factorial of 5: {fact_result}")
    
    # This will cause an error for demonstration
    undefined_variable + 10  # NameError: name 'undefined_variable' is not defined

if __name__ == "__main__":
    main()
'''

# Create C++ demo
cpp_demo = '''
/*
C++ Demo for Multi-Language Debugger
Demonstrates classes, recursion, and error handling
*/

#include <iostream>
#include <vector>
using namespace std;

class Calculator {
private:
    int precision;
    vector<string> history;
    
public:
    Calculator(int prec = 2) : precision(prec) {}
    
    int fibonacci(int n) {
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n-1) + fibonacci(n-2);
        }
    }
    
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n-1);
        }
    }
};

int main() {
    Calculator calc(2);
    
    // Test fibonacci
    int fib_result = calc.fibonacci(10);
    cout << "Fibonacci of 10: " << fib_result << endl;
    
    // Test factorial
    int fact_result = calc.factorial(5);
    cout << "Factorial of 5: " << fact_result << endl;
    
    // This will cause an error for demonstration
    // int result = 10 / 0;  // Division by zero
    
    return 0;
}
'''

# Create Java demo
java_demo = '''
/*
Java Demo for Multi-Language Debugger
Demonstrates classes, recursion, and error handling
*/

import java.util.ArrayList;

public class Calculator {
    private int precision;
    private ArrayList<String> history;
    
    public Calculator(int prec) {
        this.precision = prec;
        this.history = new ArrayList<String>();
    }
    
    public Calculator() {
        this(2);
    }
    
    public int fibonacci(int n) {
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n-1) + fibonacci(n-2);
        }
    }
    
    public int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n-1);
        }
    }
    
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        
        // Test fibonacci
        int fib_result = calc.fibonacci(10);
        System.out.println("Fibonacci of 10: " + fib_result);
        
        // Test factorial
        int fact_result = calc.factorial(5);
        System.out.println("Factorial of 5: " + fact_result);
        
        // This will cause an error for demonstration
        // int result = 10 / 0;  // ArithmeticException
    }
}
'''

# Create JavaScript demo
js_demo = '''
/*
JavaScript Demo for Multi-Language Debugger
Demonstrates functions, recursion, and error handling
*/

class Calculator {
    constructor(precision = 2) {
        this.precision = precision;
        this.history = [];
    }
    
    fibonacci(n) {
        if (n <= 1) {
            return n;
        } else {
            return this.fibonacci(n-1) + this.fibonacci(n-2);
        }
    }
    
    factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * this.factorial(n-1);
        }
    }
}

function main() {
    const calc = new Calculator();
    
    // Test fibonacci
    const fib_result = calc.fibonacci(10);
    console.log(`Fibonacci of 10: ${fib_result}`);
    
    // Test factorial
    const fact_result = calc.factorial(5);
    console.log(`Factorial of 5: ${fact_result}`);
    
    // This will cause an error for demonstration
    // undefinedVariable + 10;  // ReferenceError
}

main();
'''

# Write files to the demo directory
with open(os.path.join(demo_dir, "python_demo.py"), "w", encoding="utf-8") as f:
    f.write(python_demo)
    
with open(os.path.join(demo_dir, "cpp_demo.cpp"), "w", encoding="utf-8") as f:
    f.write(cpp_demo)
    
with open(os.path.join(demo_dir, "java_demo.java"), "w", encoding="utf-8") as f:
    f.write(java_demo)
    
with open(os.path.join(demo_dir, "js_demo.js"), "w", encoding="utf-8") as f:
    f.write(js_demo)

# Create a README for the multi-language demo
readme = '''
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
'''

with open(os.path.join(demo_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)

print(f"Multi-language demo created in '{demo_dir}' directory")
print("\nLanguages included in this demo:")
print("1. Python - Full AST analysis and debugging")
print("2. C++ - Simulated debugging with compiler support")
print("3. Java - Simulated debugging with compiler support")
print("4. JavaScript - Simulated debugging")
print("\nTo test the enhanced multi-language debugger:")
print("1. Run the application")
print("2. Select language from the initial dialog")
print("3. For C++/Java, optionally specify compiler path")
print("4. Open files or project folders")
print("5. Run analysis and step through execution")
print("6. Observe the enhanced visual feedback across languages")