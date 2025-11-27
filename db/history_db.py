"""
Database module for the Code Analysis and Debugging Visualizer
Handles session storage and retrieval using SQLite
"""

import sqlite3
import json
from datetime import datetime

class HistoryDatabase:
    def __init__(self, db_path="sessions.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize the database with the required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                code TEXT,
                analysis_results TEXT,
                execution_steps TEXT,
                variables_state TEXT,
                flow_graph TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    def save_session(self, filename, code, analysis_results, execution_steps, variables_state, flow_graph):
        """Save a session to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sessions 
            (filename, code, analysis_results, execution_steps, variables_state, flow_graph)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            filename,
            code,
            json.dumps(analysis_results),
            json.dumps(execution_steps),
            json.dumps(variables_state),
            json.dumps(flow_graph)
        ))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return session_id
        
    def load_session(self, session_id):
        """Load a session from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        
        if row:
            session_data = {
                'id': row[0],
                'filename': row[1],
                'timestamp': row[2],
                'code': row[3],
                'analysis_results': json.loads(row[4]) if row[4] else {},
                'execution_steps': json.loads(row[5]) if row[5] else [],
                'variables_state': json.loads(row[6]) if row[6] else {},
                'flow_graph': json.loads(row[7]) if row[7] else {}
            }
            conn.close()
            return session_data
            
        conn.close()
        return None
        
    def get_recent_sessions(self, limit=10):
        """Get the most recent sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, filename, timestamp 
            FROM sessions 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        sessions = [{'id': row[0], 'filename': row[1], 'timestamp': row[2]} for row in rows]
        
        conn.close()
        return sessions
        
    def delete_session(self, session_id):
        """Delete a session from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn.commit()
        conn.close()

# Example usage
if __name__ == "__main__":
    db = HistoryDatabase()
    
    # Example session data
    sample_code = "print('Hello, World!')"
    analysis_results = {"variables": [], "functions": []}
    execution_steps = [{"line": 1, "type": "Print", "description": "Print statement"}]
    variables_state = {"message": "Hello, World!"}
    flow_graph = {"nodes": [{"id": 1, "label": "print('Hello, World!')"}]}
    
    # Save a session
    session_id = db.save_session(
        "test.py", 
        sample_code, 
        analysis_results, 
        execution_steps, 
        variables_state, 
        flow_graph
    )
    print(f"Saved session with ID: {session_id}")
    
    # Load the session
    loaded_session = db.load_session(session_id)
    print("Loaded session:", loaded_session)
    
    # Get recent sessions
    recent_sessions = db.get_recent_sessions()
    print("Recent sessions:", recent_sessions)