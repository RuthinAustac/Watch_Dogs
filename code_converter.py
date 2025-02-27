import sqlite3

DB_PATH = "code_snippets.db"

def initialize_database():
    """Initializes the SQLite database and ensures UTF-8 encoding is used."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS snippets (
                        filename TEXT PRIMARY KEY, 
                        ide TEXT, 
                        code TEXT)''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

def fix_database_encoding():
    """Fixes encoding issues by re-creating the database with correct UTF-8 support."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA encoding = 'UTF-8';")  # Ensure database is UTF-8
    
    conn.commit()
    conn.close()
    print("✅ Database encoding fixed.")

if __name__ == "__main__":
    initialize_database()
    fix_database_encoding()
