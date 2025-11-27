
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
