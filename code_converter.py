import google.generativeai as genai

# Set up Gemini API key
GEMINI_API_KEY = "AIzaSyAEwM1d2DqIYlyvbmdAVFnBDy8lYuO7Nbk"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

def convert_code(code_snippet, source_lang, target_lang):
    """Converts code from one language to another using Gemini AI."""
    prompt = f"Convert the following {source_lang} code to {target_lang}:\n\n{code_snippet}"
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text if response.text else "Error: Could not generate a response."

def start_code_converter():
    """Starts the code converter module."""
    print("🔄 Code Converter module initialized.")

# Testing (optional)
if __name__ == "__main__":
    start_code_converter()
    print("EchoIDE Code Converter: Convert code using 'convert <source_lang> to <target_lang>'. Type 'exit' to stop.")

    while True:
        user_input = input("You: ").strip().lower()

        if user_input in ["exit", "quit"]:
            print("Exiting code converter...")
            break

        if user_input.startswith("convert"):
            parts = user_input.split("to")
            if len(parts) == 2:
                source_lang = parts[0].replace("convert", "").strip()
                target_lang = parts[1].strip()
                
                print(f"Enter {source_lang} code (type 'END' on a new line to finish input):")
                code_lines = []
                
                while True:
                    line = input()
                    if line.strip().upper() == "END":
                        break
                    code_lines.append(line)

                code_snippet = "\n".join(code_lines)
                converted_code = convert_code(code_snippet, source_lang, target_lang)
                print("\nConverted Code:\n", converted_code)

            else:
                print("Invalid format! Use: 'convert Python to Java'")

        else:
            print("Unknown command! Use 'convert <source_lang> to <target_lang>'")
