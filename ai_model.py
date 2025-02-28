import sqlite3
import google.generativeai as genai
import threading

# Initialize Gemini AI with API Key
GEMINI_API_KEY = ""  # Add your API key here

if not GEMINI_API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY is missing! AI features will not work.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model to Gemini 1.5 Flash

def get_saved_code(filename, ide):
    """Fetches saved code from the database based on filename and IDE."""
    try:
        with sqlite3.connect("code_snippets.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code FROM snippets WHERE filename = ? AND ide = ?", (filename, ide))
            result = cursor.fetchone()
        
        if result and result[0]:
            return f"📜 Saved Code from {ide} ({filename}):\n\n{result[0]}"
        else:
            return "❌ No saved code found for this file in the specified IDE."
    
    except sqlite3.Error as e:
        return f"❌ Database Error: {e}"

def generate_ai_response(prompt):
    """Generates an AI response using Gemini API."""
    if not GEMINI_API_KEY:
        return "⚠️ AI is currently disabled. Please set up your API key."

    try:
        response = ai_model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, "text") and response.text else "⚠️ AI response is empty."
    except Exception as e:
        return f"⚠️ Error generating AI response: {str(e)}"

def ai_assistant(query):
    """Processes user queries and retrieves code or interacts with Gemini AI."""
    words = query.lower().split()
    filename, ide = None, None

    for word in words:
        if word.endswith((".py", ".java", ".cpp", ".c", ".js")):
            filename = word
        elif "vscode" in words or "vs code" in words:
            ide = "VS Code"
        elif "pycharm" in words:
            ide = "PyCharm"
        elif "intellij" in words:
            ide = "IntelliJ IDEA"

    if filename and ide:
        return get_saved_code(filename, ide)

    return generate_ai_response(query)

def start_ai_assistant():
    """Starts AI assistant and listens for user input."""
    print("🤖 AI Assistant is now active! Type your queries or 'exit' to stop.")
    
    while True:
        query = input("🔹 Ask AI: ")
        if query.lower() == "exit":
            print("👋 Exiting AI assistant.")
            break
        print(ai_assistant(query))

def start_ai_server():
    """Runs the AI assistant in a separate thread for EchoIDE integration."""
    ai_thread = threading.Thread(target=start_ai_assistant, daemon=True)
    ai_thread.start()
