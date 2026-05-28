import subprocess
import sys
import os
import time

GROQ_API_KEY = 'YOUR_API_KEY'


DEFAULT_PYTHON_EXECUTABLE = sys.executable
GENERATED_SCRIPT_FILENAME = "generated_task.py"

def get_user_task_from_user():
    """Asks the user what task they want to perform."""
    print("\n========================================================")
    print("🚀 Android Termux AI Automation Agent Activated!")
    print("========================================================")
    print("Type anythink what you want to do..?")
    print("For exemple 'open youtube', 'create index.html with bootstrap cards', 'check storage'")
    task_query = input("\nYour request: ")
    return task_query.strip()

def call_groq_for_code_generation(task_description):
    """Calls the Groq API to get Python code optimized for Android Termux."""
    print(f"\n[1/3] 🧠 Analyzing task: '{task_description}'...")
    
    groq_prompt_template = """
Generate a self-contained, executable Python script for Android Termux environment that performs the following task.

CRITICAL INSTRUCTIONS FOR ANDROID/TERMUX:
1. YOU MUST ALWAYS INCLUDE ALL NECESSARY IMPORTS AT THE VERY TOP (e.g., 'import subprocess', 'import os', etc.). Do not forget this.
2. To open URLs, websites, or local files, ALWAYS use: subprocess.run(["termux-open", "URL_OR_PATH_HERE"])
3. For creating or manipulating files (like HTML, TXT, JS), use standard Python file operations ('with open...').
4. Return ONLY the raw executable Python code. No explanations, no markdown blocks (```python).

User's task: {}
""".format(task_description)

  
    try:
        from groq import Groq
        if GROQ_API_KEY == 'YOUR_GROQ_API_KEY_HERE' or not GROQ_API_KEY:
            print("\n❌ ERROR: कृपया कोड के ऊपर अपनी असली GROQ_API_KEY डालें।")
            return None

        client = Groq(api_key=GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert Python code generation assistant for Android Termux. You output only raw, executable code without markdown syntax."},
                {"role": "user", "content": groq_prompt_template}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1, 
        )
        
        response_content = chat_completion.choices[0].message.content.strip()
        
        if "```python" in response_content:
            response_content = response_content.split("```python")[1].split("```")[0].strip()
        elif "```" in response_content:
            response_content = response_content.split("```")[1].split("```")[0].strip()
            
        return response_content
        
    except ImportError:
        print("\n❌ ERROR: 'groq' लाइब्रेरी इंस्टॉल नहीं है।")
        print("Package install with type: pip install groq")
        return None
    except Exception as e:
        print(f"\n❌ ERROR: Groq API Key: {e}")
        return None

def save_code_to_file(code, filepath=GENERATED_SCRIPT_FILENAME):
    """Saves the generated Python code to a specified file."""
    if not code:
        print("❌ No code generated, cannot save.")
        return False
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[2/3] 💾 Generated script saved to: '{filepath}'")
        return True
    except IOError as e:
        print(f"❌ Error saving code to '{filepath}': {e}")
        return False

def execute_generated_script(script_path=GENERATED_SCRIPT_FILENAME):
    """Executes the Python script inside Termux environment."""
    if not os.path.exists(script_path):
        print(f"❌ Error: '{script_path}' file not found")
        return

    print(f"[3/3] ⚙️ Executing the generated script...\n")
    print("------------------ SCRIPT OUTPUT ------------------")
    try:
        result = subprocess.run(
            [DEFAULT_PYTHON_EXECUTABLE, script_path],
            capture_output=True, 
            text=True, 
            check=True, 
            encoding='utf-8'
        )
        print(result.stdout)
        if result.stderr:
            print("--- Errors (if any) ---")
            print(result.stderr)
        print("---------------------------------------------------")
        print("✅ Automation Task Finished Successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ Error executing script. Output logs:")
        print("--- Output ---")
        print(e.stdout)
        print("--- Errors ---")
        print(e.stderr)
    except Exception as e:
        print(f"❌ Unexpected error during script execution: {e}")

def main():
    user_request = get_user_task_from_user()
    if not user_request:
        print("No task provided. Exiting.")
        return

    generated_python_code = call_groq_for_code_generation(user_request)

    if generated_python_code:
        if save_code_to_file(generated_python_code, GENERATED_SCRIPT_FILENAME):
            execute_generated_script(GENERATED_SCRIPT_FILENAME)
        else:
            print("Failed to save the script.")
    else:
        print("Failed to get valid code from AI.")

if __name__ == "__main__":
    main()
    subprocess.run(["python", "test2.py"])
