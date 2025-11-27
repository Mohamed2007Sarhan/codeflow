
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
