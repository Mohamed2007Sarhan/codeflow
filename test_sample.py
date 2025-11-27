# Sample Python file for testing the Code Analysis and Debugging Visualizer

def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    # Test the fibonacci function
    x = 10
    y = 20
    result = fibonacci(x)
    print(f"Fibonacci of {x} is {result}")
    
    # Create a list and iterate through it
    numbers = [1, 2, 3, 4, 5]
    total = 0
    for num in numbers:
        total += num
    
    print(f"Sum of numbers: {total}")
    
    # Conditional example
    if total > 10:
        print("Total is greater than 10")
    else:
        print("Total is 10 or less")

class Calculator:
    """A simple calculator class"""
    
    def __init__(self):
        self.result = 0
        
    def add(self, a, b):
        """Add two numbers"""
        self.result = a + b
        return self.result
        
    def multiply(self, a, b):
        """Multiply two numbers"""
        self.result = a * b
        return self.result

# Run the main function
if __name__ == "__main__":
    main()