"""Simple local database connection and query helpers."""
import sqlite3
from pathlib import Path

DB_PATH = Path("data/users.db")

def create_connection(path=DB_PATH):
    """Open and configure the SQLite database connection."""
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize_schema(connection):
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL, display_name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY, user_id INTEGER, action TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    connection.commit()

def find_user_by_email(connection, email):
    return connection.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
