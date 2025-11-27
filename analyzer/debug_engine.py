"""
Debugging Engine for the Code Analysis and Debugging Visualizer
Handles execution simulation and variable tracking
"""

import ast
import copy
import traceback
import sys
import subprocess
import os
from io import StringIO

class DebuggingEngine:
    def __init__(self, source_code, filename="main.py", language="python"):
        self.source_code = source_code
        self.filename = filename
        self.language = language
        self.tree = None
        self.variables = {}
        self.execution_steps = []
        self.current_step = 0
        self.breakpoints = set()
        self.error_state = False
        self.error_line = None
        self.error_message = ""
        self.line_states = {}  # Track execution state for each line
        self.execution_flow = []  # Track execution flow for visualization
        self.call_stack = []  # Track function calls
        self.compiler_path = None  # Path to compiler for non-Python languages
        
    def set_compiler_path(self, path):
        """Set the compiler path for non-Python languages"""
        self.compiler_path = path
        
    def parse(self):
        """Parse the source code based on language"""
        if self.language.lower() == "python":
            try:
                self.tree = ast.parse(self.source_code)
                return True
            except SyntaxError as e:
                self.error_state = True
                self.error_line = e.lineno
                self.error_message = str(e)
                print(f"Syntax error in code: {e}")
                return False
        else:
            # For other languages, we'll do basic validation
            # In a real implementation, this would use language-specific parsers
            return True
            
    def execute_step(self, step_index):
        """Execute a single step of the program"""
        if self.language.lower() != "python":
            # For non-Python languages, we simulate execution
            return self.simulate_execution(step_index)
            
        if not self.tree or step_index >= len(self.execution_steps):
            return False
            
        # In a real implementation, this would execute the actual code
        # For now, we'll simulate execution and track states
        self.current_step = step_index
        
        # Simulate execution state tracking
        step = self.execution_steps[step_index]
        line_num = step['line']
        
        # Track execution flow
        if len(self.execution_flow) == 0 or self.execution_flow[-1] != line_num:
            self.execution_flow.append(line_num)
        
        # Randomly simulate some steps as successful and some as errors for demonstration
        import random
        if random.random() < 0.15:  # 15% chance of error
            self.line_states[line_num] = {
                'status': 'error',
                'message': f"Runtime error at line {line_num}: Division by zero",
                'filename': self.filename
            }
            self.error_state = True
            self.error_line = line_num
            self.error_message = f"Runtime error at line {line_num}: Division by zero"
        else:
            self.line_states[line_num] = {
                'status': 'success',
                'message': f"Executed successfully at line {line_num}",
                'filename': self.filename
            }
            
        return True
        
    def simulate_execution(self, step_index):
        """Simulate execution for non-Python languages"""
        # For non-Python languages, we create simulated steps
        if not hasattr(self, 'simulated_steps'):
            self.simulated_steps = self.create_simulated_steps()
            
        if step_index >= len(self.simulated_steps):
            return False
            
        self.current_step = step_index
        step = self.simulated_steps[step_index]
        line_num = step.get('line', step_index + 1)
        
        # Track execution flow
        if len(self.execution_flow) == 0 or self.execution_flow[-1] != line_num:
            self.execution_flow.append(line_num)
        
        # Randomly simulate some steps as successful and some as errors for demonstration
        import random
        if random.random() < 0.15:  # 15% chance of error
            self.line_states[line_num] = {
                'status': 'error',
                'message': f"Runtime error at line {line_num}: Execution failed",
                'filename': self.filename
            }
            self.error_state = True
            self.error_line = line_num
            self.error_message = f"Runtime error at line {line_num}: Execution failed"
        else:
            self.line_states[line_num] = {
                'status': 'success',
                'message': f"Executed successfully at line {line_num}",
                'filename': self.filename
            }
            
        return True
        
    def create_simulated_steps(self):
        """Create simulated execution steps for non-Python languages"""
        lines = self.source_code.split('\n')
        steps = []
        for i, line in enumerate(lines):
            if line.strip():  # Only create steps for non-empty lines
                steps.append({
                    'line': i + 1,
                    'type': 'Statement',
                    'description': f"Executing statement at line {i + 1}",
                    'filename': self.filename
                })
        return steps
        
    def step_forward(self):
        """Move one step forward in execution"""
        if self.language.lower() != "python":
            if not hasattr(self, 'simulated_steps'):
                self.simulated_steps = self.create_simulated_steps()
            if self.current_step < len(self.simulated_steps) - 1:
                self.current_step += 1
                return self.simulate_execution(self.current_step)
            return False
            
        if self.current_step < len(self.execution_steps) - 1:
            self.current_step += 1
            return self.execute_step(self.current_step)
        return False
        
    def step_back(self):
        """Move one step backward in execution"""
        if self.current_step > 0:
            self.current_step -= 1
            # Reset state to this step
            return True
        return False
        
    def run_to_end(self):
        """Run execution to the end"""
        if self.language.lower() != "python":
            if not hasattr(self, 'simulated_steps'):
                self.simulated_steps = self.create_simulated_steps()
            while self.current_step < len(self.simulated_steps) - 1:
                if not self.step_forward():
                    return False
            return True
            
        while self.current_step < len(self.execution_steps) - 1:
            if not self.step_forward():
                return False
        return True
        
    def set_breakpoint(self, line_number):
        """Set a breakpoint at the specified line"""
        self.breakpoints.add(line_number)
        
    def remove_breakpoint(self, line_number):
        """Remove a breakpoint at the specified line"""
        self.breakpoints.discard(line_number)
        
    def get_current_variables(self):
        """Get the current state of variables"""
        return copy.deepcopy(self.variables)
        
    def get_execution_timeline(self):
        """Get the execution timeline"""
        if self.language.lower() != "python":
            return getattr(self, 'simulated_steps', [])[:self.current_step+1]
        return self.execution_steps[:self.current_step+1]
        
    def get_line_state(self, line_number):
        """Get the execution state for a specific line"""
        return self.line_states.get(line_number, {'status': 'pending', 'message': 'Not executed yet', 'filename': self.filename})
        
    def has_error(self):
        """Check if there's an error in execution"""
        return self.error_state
        
    def get_error_info(self):
        """Get error information"""
        return {
            'has_error': self.error_state,
            'line': self.error_line,
            'message': self.error_message,
            'filename': self.filename
        }
        
    def reset_execution(self):
        """Reset the execution state"""
        self.current_step = 0
        self.error_state = False
        self.error_line = None
        self.error_message = ""
        self.line_states = {}
        self.execution_flow = []
        self.call_stack = []
        
    def get_execution_flow(self):
        """Get the execution flow for visualization"""
        return self.execution_flow
        
    def get_call_stack(self):
        """Get the current call stack"""
        return self.call_stack
        
    def initialize_execution_steps(self):
        """Initialize the execution steps based on the language"""
        if self.language.lower() == "python":
            if not self.tree:
                return
                
            # Clear previous steps
            self.execution_steps = []
                
            # Walk the tree and create execution steps
            for node in ast.walk(self.tree):
                if hasattr(node, 'lineno'):
                    lineno = getattr(node, 'lineno', 0)
                    if lineno > 0:  # Only add steps with valid line numbers
                        step = {
                            'line': lineno,
                            'type': type(node).__name__,
                            'description': f"Executing {type(node).__name__} at line {lineno}",
                            'filename': self.filename
                        }
                        self.execution_steps.append(step)
                    
            # Sort steps by line number
            self.execution_steps.sort(key=lambda x: x['line'])
        else:
            # For non-Python languages, create simulated steps
            self.simulated_steps = self.create_simulated_steps()

# Example usage
if __name__ == "__main__":
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

x = 10
y = 20
result = fibonacci(x)
print(result)
"""
    
    engine = DebuggingEngine(sample_code)
    if engine.parse():
        engine.initialize_execution_steps()
        print("Execution steps:", engine.execution_steps)