import sqlite3
from pathlib import Path

DB_PATH = Path("task_dashboard.db")

def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database and create tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Task (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT,
            Due_Date TEXT NOT NULL,
            Status TEXT NOT NULL,
            Created_At TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    
    conn.commit()
    conn.close()

