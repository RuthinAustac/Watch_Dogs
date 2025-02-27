import threading
from ai_model import start_ai_server


from code_converter import start_code_converter
from ide_watcher import start_ide_watcher as start_file_watcher

from database import initialize_database

from code_storage import initialize_code_storage

from ide_monitor import start_ide_monitor

def main():
    print("🚀 EchoIDE is starting...")

    # Initialize database and storage (No need for separate threads)
    initialize_database()
    initialize_code_storage()

    # Creating threads for modules that need to run continuously
    threads = [
        threading.Thread(target=start_ai_server, daemon=True),
        threading.Thread(target=start_code_converter, daemon=True),
        threading.Thread(target=start_file_watcher, daemon=True),
        threading.Thread(target=start_ide_monitor, daemon=True)
    ]

    # Starting all threads
    for thread in threads:
        thread.start()

    print("✅ EchoIDE is running! Monitoring IDEs and ready for AI assistance.")
    
    try:
        while True:
            pass  # Keeps main thread alive while background threads run
    except KeyboardInterrupt:
        print("\n🛑 Stopping EchoIDE...")

if __name__ == "__main__":
    main()
