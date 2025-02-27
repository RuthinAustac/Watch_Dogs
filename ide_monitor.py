import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from code_storage import save_code

WATCHED_DIRECTORIES = [
    r"D:\EchoIDE",
    r"C:\Users\ruthi\PycharmProjects\MyPythonProject",
    r"C:\Users\ruthi\IdeaProjects\E-commerceapp"
]

class CodeMonitor(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        
        filepath = event.src_path
        filename = os.path.basename(filepath)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
            
            ide = self.get_ide(filepath)

            if ide:
                save_code(filename, "Unknown", code, ide)
                print(f"✅ Code saved: {filename} from {ide}")

        except Exception as e:
            print(f"⚠️ Error reading file {filename}: {e}")

    def get_ide(self, filepath):
        if WATCHED_DIRECTORIES[0] in filepath:
            return "VS Code"
        elif WATCHED_DIRECTORIES[1] in filepath:
            return "PyCharm"
        elif WATCHED_DIRECTORIES[2] in filepath:
            return "IntelliJ IDEA"
        return None

def start_ide_monitor():
    """Starts the IDE file monitoring system."""
    observer = Observer()
    event_handler = CodeMonitor()

    for directory in WATCHED_DIRECTORIES:
        if os.path.exists(directory):
            observer.schedule(event_handler, directory, recursive=True)

    observer.start()
    print("🚀 IDE Monitor started... Press CTRL+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

# Testing (optional)
if __name__ == "__main__":
    start_ide_monitor()
