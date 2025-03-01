import sqlite3
import google.generativeai as genai
import threading

# Initialize Gemini AI with API Key
GEMINI_API_KEY = "AIzaSyAEwM1d2DqIYlyvbmdAVFnBDy8lYuO7Nbk"  # Add your API key here

if not GEMINI_API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY is missing! AI features will not work.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model to Gemini 1.5 Flash

# Global variables to store last retrieved code and language
last_retrieved_code = None
last_code_language = None

def get_saved_code(filename, ide):
    """Fetches the latest saved code from the database for a given file and IDE."""
    global last_retrieved_code, last_code_language

    try:
        with sqlite3.connect("code_snippets.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, language FROM snippets 
                WHERE filename = ? AND ide = ? 
                ORDER BY timestamp DESC LIMIT 1
            """, (filename, ide))
            result = cursor.fetchone()

        if result and result[0]:
            last_retrieved_code = result[0]  # Store for conversion
            last_code_language = result[1]  # Store language

            print(f"🔍 [AI Retrieval] Latest Code for {filename} from {ide}:\n{result[0][:100]}...")  # ✅ Debugging Log
            return f"📜 Latest Saved Code from {ide} ({filename}):\n\n{result[0]}"
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

def convert_code(target_language):
    """Converts last retrieved code to the specified language."""
    if not last_retrieved_code or not last_code_language:
        return "❌ No previously retrieved code found. Please retrieve a file first."

    if last_code_language.lower() == target_language.lower():
        return "⚠️ The code is already in the requested language."

    conversion_prompt = f"Convert the following {last_code_language} code to {target_language}:\n\n{last_retrieved_code}"
    return generate_ai_response(conversion_prompt)

def ai_assistant(query):
    """Processes user queries and retrieves code or interacts with Gemini AI."""
    words = query.lower().split()
    filename, ide, target_language = None, None, None

    # Detect filename & IDE
    for word in words:
        if word.endswith((".py", ".java", ".cpp", ".c", ".js")):
            filename = word
        elif "vscode" in words or "vs code" in words:
            ide = "VS Code"
        elif "pycharm" in words:
            ide = "PyCharm"
        elif "intellij" in words:
            ide = "IntelliJ IDEA"

    # Detect conversion request
    if "convert" in words:
        if "python" in words:
            target_language = "Python"
        elif "java" in words:
            target_language = "Java"
        elif "c++" in words or "cpp" in words:
            target_language = "C++"
        elif "c" in words:
            target_language = "C"
        elif "javascript" in words or "js" in words:
            target_language = "JavaScript"

    if filename and ide:
        return get_saved_code(filename, ide)

    if target_language:
        return convert_code(target_language)

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
