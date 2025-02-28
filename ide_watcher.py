import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database import CodeDatabase
import time

db = CodeDatabase()

class IDEWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        """Handles file modifications and saves updated code to the database."""
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)
        if filename.endswith((".db", ".db-wal", ".db-shm")):  
            return  # ❌ Ignore database system files  

        ide = detect_ide(event.src_path)  # Detect IDE (VS Code, PyCharm, etc.)
        language = detect_language(filename)  # Detect programming language

        print(f"🔄 File modified: {event.src_path}")  # ✅ Debugging log

        try:
            with open(event.src_path, "r", encoding="utf-8") as f:
                new_code = f.read().strip()  # ✅ Strip to remove accidental whitespace differences

            if not new_code:
                print(f"⚠️ Skipping empty file: {filename}")
                return

            # ✅ Fetch last saved version to check for changes
            last_saved_code = db.get_code(filename, ide).strip()
            print(f"🔍 Previous Code in DB for {filename}:\n{last_saved_code[:100]}...")
            print(f"🔍 New Code from File for {filename}:\n{new_code[:100]}...")

            if last_saved_code == new_code:
                print(f"⚠️ No changes detected in {filename}, skipping update.")
                return

            print(f"✅ Code change detected! Updating database for {filename}")
            db.save_code(filename, ide, language, new_code)  # ✅ Save Updated Code
        except Exception as e:
            print(f"❌ Error reading file {filename}: {e}")

def detect_ide(file_path):
    """Detects which IDE is being used based on the file path."""
    if "VSCode" in file_path or ".vscode" in file_path:
        return "VS Code"
    elif "PyCharm" in file_path:
        return "PyCharm"
    elif "IntelliJ" in file_path:
        return "IntelliJ IDEA"
    return "Unknown"

def detect_language(filename):
    """Detects the language based on file extension."""
    ext = filename.split(".")[-1]
    language_map = {
        "py": "Python",
        "java": "Java",
        "cpp": "C++",
        "c": "C",
        "js": "JavaScript"
    }
    return language_map.get(ext, "Unknown")

def start_watcher():
    """Starts the file watcher."""
    path = os.getcwd()  # ✅ Monitor current working directory
    event_handler = IDEWatcher()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print("👀 Watching for file changes in:", path)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()
