"""
Comprehensive demonstration of the enhanced Code Analysis and Debugging Visualizer
This script creates multiple Python files to demonstrate project-level debugging
"""

import os

# Create a project directory
project_dir = "demo_project"
os.makedirs(project_dir, exist_ok=True)

# Create main.py
main_py = '''
"""
Main module for the demo project
Demonstrates cross-module function calls and error handling
"""

from utils import calculate_square, process_list
from models import DataProcessor

def main():
    """Main function demonstrating various debugging scenarios"""
    print("Starting demo project...")
    
    # Test utility functions
    x = 5
    squared = calculate_square(x)
    print(f"Square of {x} is {squared}")
    
    # Test list processing
    data = [1, 2, 3, 4, 5]
    processed = process_list(data)
    print(f"Processed data: {processed}")
    
    # Test class functionality
    processor = DataProcessor("Demo Processor")
    result = processor.process_item(10)
    print(f"Processed item result: {result}")
    print(f"Processor stats: {processor.get_stats()}")
    
    # This will cause an error for demonstration
    undefined_variable + 10  # NameError: name 'undefined_variable' is not defined

if __name__ == "__main__":
    main()
'''

# Create utils.py
utils_py = '''
"""
Utility functions for the demo project
"""

def calculate_square(n):
    """Calculate the square of a number"""
    return n * n

def process_list(data_list):
    """Process a list of numbers"""
    results = []
    total = 0
    
    for item in data_list:
        if item > 0:
            squared = item ** 2
            results.append(squared)
            total += squared
        elif item < 0:
            # This will cause an error for negative numbers
            invalid_result = 1 / item  # Division by zero or negative
            results.append(invalid_result)
        else:
            results.append(0)
    
    return results, total
'''

# Create models.py
models_py = '''
"""
Model classes for the demo project
"""

class DataProcessor:
    """A class for processing data"""
    
    def __init__(self, name):
        self.name = name
        self.processed_count = 0
        
    def process_item(self, item):
        """Process a single item"""
        self.processed_count += 1
        return item * 2
        
    def get_stats(self):
        """Get processing statistics"""
        return {
            'name': self.name,
            'processed': self.processed_count
        }
'''

# Create a test file with more complex structures
complex_py = '''
"""
Complex module with advanced Python constructs
"""

import math

class ComplexCalculator:
    """A complex calculator with multiple methods"""
    
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
            
    def is_prime(self, n):
        """Check if number is prime"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
        
    def process_sequence(self, start, end):
        """Process a sequence of numbers"""
        results = {}
        for num in range(start, end + 1):
            results[num] = {
                'fibonacci': self.fibonacci(num) if num < 10 else "Too large",
                'factorial': self.factorial(num) if num < 10 else "Too large",
                'is_prime': self.is_prime(num)
            }
        return results

def main():
    """Main function for complex module"""
    calc = ComplexCalculator()
    
    # Test fibonacci
    fib_result = calc.fibonacci(8)
    print(f"Fibonacci of 8: {fib_result}")
    
    # Test factorial
    fact_result = calc.factorial(5)
    print(f"Factorial of 5: {fact_result}")
    
    # Test prime checking
    prime_check = calc.is_prime(17)
    print(f"Is 17 prime? {prime_check}")
    
    # Test sequence processing
    sequence_results = calc.process_sequence(1, 5)
    print("Sequence results:")
    for num, data in sequence_results.items():
        print(f"  {num}: {data}")
        
    # This will cause an error for demonstration
    result = 10 / 0  # ZeroDivisionError

if __name__ == "__main__":
    main()
'''

# Write files to the project directory
with open(os.path.join(project_dir, "main.py"), "w", encoding="utf-8") as f:
    f.write(main_py)
    
with open(os.path.join(project_dir, "utils.py"), "w", encoding="utf-8") as f:
    f.write(utils_py)
    
with open(os.path.join(project_dir, "models.py"), "w", encoding="utf-8") as f:
    f.write(models_py)
    
with open(os.path.join(project_dir, "complex.py"), "w", encoding="utf-8") as f:
    f.write(complex_py)

# Create a README for the demo project
readme = '''
# Demo Project for Code Analysis and Debugging Visualizer

This project demonstrates the capabilities of the enhanced debugging visualizer.

## Files Included

1. **main.py** - Entry point demonstrating cross-module function calls
2. **utils.py** - Utility functions with error conditions
3. **models.py** - Class definitions
4. **complex.py** - Advanced Python constructs (recursion, classes, math)

## Features Demonstrated

- Multi-file project debugging
- Cross-module function calls
- Class instantiation and method calls
- Error conditions (ZeroDivisionError, NameError)
- Recursive functions
- Loop constructs
- Conditional statements
- Exception handling

## How to Use with the Debugger

1. Open the project folder in the Code Analysis and Debugging Visualizer
2. Select any file to debug from the file selector
3. Run analysis to see code structure
4. Step through execution with visual feedback
5. Observe:
   - Green lines: Successfully executed
   - Red lines: Errors detected
   - Blue line: Currently executing
   - Timeline indicators: [SUCCESS] (success), [ERROR] (error), [PENDING] (pending), [CURRENT] (current)
6. Switch between files using the file selector
7. View execution flow graph in the Flow Graph tab
'''

with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)

print(f"Demo project created in '{project_dir}' directory")
print("\nFeatures included in this demo:")
print("1. Multi-file project structure")
print("2. Cross-module function calls")
print("3. Class definitions and instantiations")
print("4. Error conditions (ZeroDivisionError, NameError)")
print("5. Recursive functions")
print("6. Loop constructs")
print("7. Conditional statements")
print("8. Exception handling")
print("\nTo test the enhanced debugger:")
print("1. Open the project folder in the Code Analysis and Debugging Visualizer")
print("2. Select any file to debug using the file selector")
print("3. Run analysis and step through execution")
print("4. Observe the enhanced visual feedback:")
print("   - Color-coded line highlighting")
print("   - Timeline status indicators")
print("   - Execution flow tracking")
print("   - Cross-file navigation")
print("   - Flow graph visualization")