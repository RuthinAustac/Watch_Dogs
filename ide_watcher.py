import os
import time
import sqlite3

WATCHED_DIRECTORIES = {
    "IntelliJ IDEA": "C:\\Users\\ruthi\\IdeaProjects\\E-commerceapp\\src\\ecommerce",
    "VS Code": "D:\\Projects\\VSCodeProject",  # Add correct path for VS Code
    "PyCharm": "D:\\Projects\\PyCharmProject"  # Add correct path for PyCharm
}

DB_PATH = "code_snippets.db"

def save_code_snippet(filename, ide, code):
    """Saves the complete code snippet into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS snippets (
                        filename TEXT, ide TEXT, code TEXT, PRIMARY KEY (filename, ide))''')
    
    cursor.execute("INSERT OR REPLACE INTO snippets (filename, ide, code) VALUES (?, ?, ?)",
                   (filename, ide, code))
    
    conn.commit()
    conn.close()
    print(f"✅ Code saved: {filename} from {ide}")

def monitor_directory(path, ide):
    """Monitors the directory for file changes."""
    file_mod_times = {}

    while True:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".java", ".py", ".cpp")) and not file.endswith("~"):
                    full_path = os.path.join(root, file)
                    try:
                        mod_time = os.path.getmtime(full_path)
                        if file not in file_mod_times or file_mod_times[file] != mod_time:
                            file_mod_times[file] = mod_time
                            
                            with open(full_path, "r", encoding="utf-8") as f:
                                code = f.read()
                                
                            save_code_snippet(file, ide, code)
                    except Exception as e:
                        print(f"⚠️ Error reading {file}: {e}")
        time.sleep(2)  # Check for changes every 2 seconds

# ✅ Fix: Ensure start_ide_watcher() is defined
def start_ide_watcher():
    """Starts watching directories for all IDEs."""
    print("🔍 Watching directories for code changes...")
    for ide, directory in WATCHED_DIRECTORIES.items():
        print(f"📂 Monitoring {directory} for {ide}")
        monitor_directory(directory, ide)
