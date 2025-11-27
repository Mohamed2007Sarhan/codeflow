
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
