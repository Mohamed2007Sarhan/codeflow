
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
