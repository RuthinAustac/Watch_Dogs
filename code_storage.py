import sqlite3

def initialize_code_storage():
    """Creates the code storage table if not exists."""
    conn = sqlite3.connect("code_snippets.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            language TEXT NOT NULL,
            code TEXT NOT NULL,
            ide TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Code storage initialized successfully!")

def save_code(filename, language, code, ide):
    """Saves the code snippet into the database."""
    conn = sqlite3.connect("code_snippets.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO snippets (filename, language, code, ide) 
        VALUES (?, ?, ?, ?)
    """, (filename, language, code, ide))

    conn.commit()
    conn.close()
    print(f"✅ Code snippet saved: {filename}")

if __name__ == "__main__":
    initialize_code_storage()
