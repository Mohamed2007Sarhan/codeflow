"""
Flow Graph Visualization for the Code Analysis and Debugging Visualizer
Handles the creation and rendering of execution flow graphs
"""

import matplotlib.pyplot as plt
import networkx as nx
import base64
from io import BytesIO

class FlowGraphVisualizer:
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_node(self, node_id, label, node_type="operation"):
        """Add a node to the flow graph"""
        self.graph.add_node(node_id, label=label, type=node_type)
        
    def add_edge(self, from_node, to_node, label=""):
        """Add an edge between nodes"""
        self.graph.add_edge(from_node, to_node, label=label)
        
    def generate_flow_graph(self, execution_steps):
        """Generate a flow graph from execution steps"""
        self.graph.clear()
        
        # Add nodes for each execution step
        for i, step in enumerate(execution_steps):
            node_id = f"step_{i}"
            label = f"{step['type']}\nLine {step['line']}"
            self.add_node(node_id, label)
            
        # Add edges to show flow (simplified linear flow for now)
        for i in range(len(execution_steps) - 1):
            self.add_edge(f"step_{i}", f"step_{i+1}", "next")
            
        return self.graph
        
    def render_to_image(self, width=8, height=6):
        """Render the flow graph to an image"""
        plt.figure(figsize=(width, height))
        
        # Use shell layout for better visualization
        pos = nx.shell_layout(self.graph)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, node_color='lightblue', node_size=1500)
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray', arrows=True, arrowsize=20)
        
        # Draw labels
        labels = nx.get_node_attributes(self.graph, 'label')
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=8)
        
        # Draw edge labels
        edge_labels = nx.get_edge_attributes(self.graph, 'label')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=6)
        
        plt.axis('off')
        
        # Save to base64 image
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return image_base64
        
    def get_graph_data(self):
        """Get the graph data in a serializable format"""
        nodes = []
        edges = []
        
        for node, data in self.graph.nodes(data=True):
            nodes.append({
                'id': node,
                'label': data.get('label', ''),
                'type': data.get('type', 'unknown')
            })
            
        for source, target, data in self.graph.edges(data=True):
            edges.append({
                'source': source,
                'target': target,
                'label': data.get('label', '')
            })
            
        return {
            'nodes': nodes,
            'edges': edges
        }

# Example usage
if __name__ == "__main__":
    # Sample execution steps
    execution_steps = [
        {'line': 1, 'type': 'FunctionDef', 'description': 'Define fibonacci function'},
        {'line': 2, 'type': 'If', 'description': 'Check if n <= 1'},
        {'line': 3, 'type': 'Return', 'description': 'Return n'},
        {'line': 5, 'type': 'Return', 'description': 'Recursive call'},
        {'line': 8, 'type': 'Assign', 'description': 'Assign x = 10'},
        {'line': 9, 'type': 'Assign', 'description': 'Assign result = fibonacci(x)'},
        {'line': 10, 'type': 'Print', 'description': 'Print result'}
    ]
    
    # Create and generate flow graph
    visualizer = FlowGraphVisualizer()
    graph = visualizer.generate_flow_graph(execution_steps)
    
    # Render to image
    image_data = visualizer.render_to_image()
    print(f"Generated flow graph image (first 100 chars): {image_data[:100]}...")
    
    # Get graph data
    graph_data = visualizer.get_graph_data()
    print(f"Graph data: {graph_data}")