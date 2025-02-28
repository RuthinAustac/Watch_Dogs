import sqlite3

DB_PATH = "code_snippets.db"

# Persistent connection
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

def initialize_code_storage():
    """Creates the code storage table if it doesn't exist."""
    try:
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
        print("✅ Code storage initialized successfully!")
    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")

def save_code(filename, language, code, ide):
    """Saves the code snippet into the database with UTF-8 encoding fix."""
    if not language:
        print(f"⚠️ Error: Language must be provided for {filename}!")
        return

    try:
        # Ensure UTF-8 encoding to prevent db errors
        encoded_code = code.encode("utf-8", "ignore").decode("utf-8")
        
        cursor.execute("""
            INSERT INTO snippets (filename, language, code, ide) 
            VALUES (?, ?, ?, ?)
        """, (filename, language, encoded_code, ide))
        
        conn.commit()
        print(f"✅ Code snippet saved: {filename} from {ide}")
    
    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    initialize_code_storage()
    print("🔍 Database ready. Use save_code() to insert data.")
