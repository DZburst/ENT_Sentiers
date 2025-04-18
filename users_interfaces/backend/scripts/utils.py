import sqlite3
import json
import os

# Absolute path to school.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of utils.py
DB_PATH = os.path.join(BASE_DIR, '..', 'school.db')  # Go up one level to backend/

def get_db_connection():
    """Establish a connection to the SQLite database and enable foreign key support."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable access by column name
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return conn, cursor

def close_db_connection(conn, cursor):
    """Commit changes and close the database connection."""
    conn.commit()
    cursor.close()
    conn.close()

def load_json_file(file_path):
    """Load and return data from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}. Details: {e}")
        return None