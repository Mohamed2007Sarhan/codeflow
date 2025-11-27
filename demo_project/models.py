
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
