"""
AST Analyzer for Python code
This module parses Python code and extracts structural information
"""

import ast

class ASTAnalyzer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tree = None
        self.variables = []
        self.functions = []
        self.classes = []
        self.conditionals = []
        self.loops = []
        
    def parse(self):
        """Parse the source code into an AST"""
        try:
            self.tree = ast.parse(self.source_code)
            return True
        except SyntaxError as e:
            print(f"Syntax error in code: {e}")
            return False
            
    def extract_variables(self):
        """Extract variable assignments from the AST"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        # Convert the assigned value to string representation
                        try:
                            value_str = ast.dump(node.value)[:50] + "..." if len(ast.dump(node.value)) > 50 else ast.dump(node.value)
                        except:
                            value_str = "Unknown"
                            
                        self.variables.append({
                            'name': target.id,
                            'line': getattr(node, 'lineno', 0),
                            'value': value_str
                        })
                        
    def extract_functions(self):
        """Extract function definitions from the AST"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                params = [arg.arg for arg in node.args.args]
                self.functions.append({
                    'name': node.name,
                    'line': getattr(node, 'lineno', 0),
                    'params': params,
                    'returns': None  # Would need to parse return statements separately
                })
                
    def extract_classes(self):
        """Extract class definitions from the AST"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                attributes = []
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                attributes.append(target.id)
                                
                self.classes.append({
                    'name': node.name,
                    'line': getattr(node, 'lineno', 0),
                    'methods': methods,
                    'attributes': attributes
                })
                
    def extract_conditionals(self):
        """Extract conditional statements from the AST"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.If):
                # Convert the test condition to string representation
                try:
                    test_str = ast.dump(node.test)[:50] + "..." if len(ast.dump(node.test)) > 50 else ast.dump(node.test)
                except:
                    test_str = "Unknown"
                    
                self.conditionals.append({
                    'line': getattr(node, 'lineno', 0),
                    'type': 'if',
                    'test': test_str
                })
                
    def extract_loops(self):
        """Extract loop statements from the AST"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.For, ast.While)):
                loop_type = 'for' if isinstance(node, ast.For) else 'while'
                
                if isinstance(node, ast.For):
                    try:
                        target_str = ast.dump(node.target)[:30] + "..." if len(ast.dump(node.target)) > 30 else ast.dump(node.target)
                    except:
                        target_str = "Unknown"
                    self.loops.append({
                        'line': getattr(node, 'lineno', 0),
                        'type': loop_type,
                        'target': target_str,
                        'test': None
                    })
                else:  # While loop
                    try:
                        test_str = ast.dump(node.test)[:50] + "..." if len(ast.dump(node.test)) > 50 else ast.dump(node.test)
                    except:
                        test_str = "Unknown"
                    self.loops.append({
                        'line': getattr(node, 'lineno', 0),
                        'type': loop_type,
                        'target': None,
                        'test': test_str
                    })
                
    def analyze(self):
        """Perform complete analysis of the source code"""
        if not self.parse():
            return False
            
        self.extract_variables()
        self.extract_functions()
        self.extract_classes()
        self.extract_conditionals()
        self.extract_loops()
        
        return True
        
    def get_results(self):
        """Return all analysis results"""
        return {
            'variables': self.variables,
            'functions': self.functions,
            'classes': self.classes,
            'conditionals': self.conditionals,
            'loops': self.loops
        }

# Example usage
if __name__ == "__main__":
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    x = 10
    y = 20
    result = fibonacci(x)
    print(result)
    
class Calculator:
    def __init__(self):
        self.result = 0
        
    def add(self, a, b):
        self.result = a + b
        return self.result

for i in range(5):
    print(i)
"""
    
    analyzer = ASTAnalyzer(sample_code)
    if analyzer.analyze():
        results = analyzer.get_results()
        print("Variables:", results['variables'])
        print("Functions:", results['functions'])
        print("Classes:", results['classes'])
        print("Conditionals:", results['conditionals'])
        print("Loops:", results['loops'])