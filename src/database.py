import sqlite3
import os

# Database will be created in the src directory
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vdbc.db')

def init_db():
    """Initialize the database with minimal required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create a simple table for shared sessions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shared_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        session_url TEXT NOT NULL,
        trial_name TEXT NOT NULL,
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized at {DB_PATH}")