import sqlite3
import threading
import time

class CodeDatabase:
    def __init__(self, db_path="code_snippets.db"):
        self.db_path = db_path
        self.lock = threading.Lock()  # ✅ Prevents multiple threads from accessing DB at once
        self.connect_db()

    def connect_db(self):
        """Establishes a database connection with a timeout to avoid lock issues."""
        retries = 5  # 🔄 Retries if database is locked
        for attempt in range(retries):
            try:
                self.conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=10)
                self.cursor = self.conn.cursor()
                self.conn.execute("PRAGMA journal_mode=WAL;")  # ✅ Improves write safety
                self.conn.execute("PRAGMA synchronous=NORMAL;")  # ✅ Prevents excessive I/O blocking
                self.conn.execute("PRAGMA encoding='UTF-8';")  # ✅ Ensures proper encoding
                self.create_table()
                print("✅ Database connected successfully.")
                return
            except sqlite3.OperationalError as e:
                print(f"⚠️ Database connection attempt {attempt + 1} failed: {e}")
                time.sleep(1)
        raise sqlite3.OperationalError("❌ Failed to connect to database after multiple attempts.")

    def create_table(self):
        """Creates the snippets table if it doesn't exist."""
        with self.lock:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS snippets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    ide TEXT NOT NULL,
                    language TEXT NOT NULL DEFAULT 'Unknown',
                    code TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()

    def save_code(self, filename, ide, language, code):
        """Saves or updates a code snippet. Deletes old versions to keep only the latest."""
        with self.lock:
            try:
                # ✅ Delete any old entries to keep the latest one
                print(f"🗑️ Deleting old versions of {filename} from {ide} before updating.")
                self.cursor.execute("""
                    DELETE FROM snippets WHERE filename = ? AND ide = ?
                """, (filename, ide))

                # ✅ Insert the new updated version
                self.cursor.execute("""
                    INSERT INTO snippets (filename, ide, language, code, timestamp) 
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (filename, ide, language, code))
                self.conn.commit()
                print(f"✅ Code updated in DB: {filename} from {ide}")
            except sqlite3.OperationalError as e:
                print(f"❌ Database locked error: {e}. Retrying...")
                self.reconnect_db()
                self.save_code(filename, ide, language, code)

    def get_code(self, filename, ide):
        """Retrieves the latest saved code for a given file and IDE."""
        with self.lock:
            try:
                self.conn.commit()  # ✅ Ensure fresh data is fetched
                self.cursor.execute("""
                    SELECT code FROM snippets 
                    WHERE filename = ? AND ide = ? 
                    ORDER BY timestamp DESC LIMIT 1
                """, (filename, ide))
                result = self.cursor.fetchone()
                return result[0] if result else ""
            except sqlite3.OperationalError as e:
                print(f"❌ Database locked error: {e}. Retrying...")
                self.reconnect_db()
                return self.get_code(filename, ide)

    def reconnect_db(self):
        """Reconnects to the database to fix locking issues."""
        print("♻️ Reconnecting to database to resolve locking issue...")
        self.conn.close()
        time.sleep(1)
        self.connect_db()
        print("✅ Database reconnected successfully!")

if __name__ == "__main__":
    db = CodeDatabase()
    print("📂 Database setup complete.")
