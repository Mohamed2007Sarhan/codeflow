
"""
Sample Python Application for Debugging Demonstration
This file demonstrates various Python constructs that our debugger can analyze
"""

# Variable assignments
name = "Debugging Visualizer"
version = 1.0
debug_mode = True

# Function definitions
def calculate_factorial(n):
    """Calculate factorial of n"""
    if n <= 1:
        return 1
    else:
        return n * calculate_factorial(n - 1)

def process_data(data_list):
    """Process a list of data"""
    results = []
    total = 0
    
    # Loop through data
    for item in data_list:
        # Conditional processing
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

# Class definition
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

# Main execution
if __name__ == "__main__":
    # Test factorial function
    fact_result = calculate_factorial(5)
    print(f"Factorial of 5: {fact_result}")
    
    # Test data processing
    test_data = [1, 2, 3, -1, 0, 4]
    try:
        processed_data, total = process_data(test_data)
        print(f"Processed data: {processed_data}")
        print(f"Total: {total}")
    except Exception as e:
        print(f"Error processing data: {e}")
    
    # Test class
    processor = DataProcessor("Demo Processor")
    result = processor.process_item(10)
    print(f"Processed item result: {result}")
    print(f"Processor stats: {processor.get_stats()}")
    
    # This will cause an error for demonstration
    undefined_variable + 10  # NameError: name 'undefined_variable' is not defined
