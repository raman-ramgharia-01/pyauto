import subprocess
import sys
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Use the same Python interpreter that is running this script
DEFAULT_PYTHON_EXECUTABLE = sys.executable
GENERATED_SCRIPT_FILENAME = "generated_task.py"

simulated_response = ''' '''

def get_user_task_from_user():
    """Asks the user what task they want to perform."""
    print("Hello! I can help you generate and run Python scripts for simple tasks.")
    print("What task would you like to automate? Please be descriptive.")
    print("Examples: 'open notepad', 'create file named my_notes.txt with content Hello there', 'run a simple web search for 'latest python news''")
    task_query = input("Your request: ")
    return task_query.strip()

def call_groq_for_code_generation(task_description):
    """
    This function simulates calling the Groq API to get Python code.
    In a real implementation, you would use the 'groq' Python library or 'requests'
    to interact with the Groq API.
    """
    print(f"\n--- Simulating Groq API call for task: '{task_description}' ---")

    # Construct a prompt for Groq. This prompt guides the AI to generate Python code.
    groq_prompt_template = """
Generate a self-contained Python script that performs the following task.
Use the 'subprocess' module for system commands like opening applications or creating/writing files.
If the task involves file creation, include the filename and content if provided in the request.
If the task involves external information (like web search), use appropriate Python libraries or simulate it appropriately if direct external access is restricted.
Return ONLY the Python code block, no explanations, introductions, or markdown formatting.
Ensure the generated code is executable directly.

User's task: {}
""".format(task_description)

    simulated_response = ""
  
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        print("Calling Groq API...")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert Python code generation assistant. Provide only executable Python code."},
                {"role": "user", "content": groq_prompt_template}
            ],
            model="llama-3.3-70b-versatile", # Or another suitable Groq model like 'mixtral-8x7b-32768'
            temperature=0.1, # Lower temperature for more deterministic code generation
        )
        simulated_response = chat_completion.choices[0].message.content
        if simulated_response.startswith("```python"):
            simulated_response = simulated_response[9:]  # Remove ```python
        if simulated_response.endswith("```"):
            simulated_response = simulated_response[:-3]  # Remove ```
        simulated_response = simulated_response.strip()
        print("Groq API call successful.")
    except ImportError:
        print("\nERROR: The 'groq' library is not installed.")
        print("Please install it by running: pip install groq")
        return None
    except Exception as e:
        print(f"\nERROR: An error occurred while calling Groq API: {e}")
        print("Please ensure your GROQ_API_KEY is correct and that the API is accessible.")
 
 
    if not simulated_response:
        print("Groq API (simulated) returned no code.")
        return None
        
    print("--- Simulated Groq response received ---")
    return simulated_response.strip()

def save_code_to_file(code, filepath=GENERATED_SCRIPT_FILENAME):
    """Saves the generated Python code to a specified file."""
    if not code:
        print("No code generated, cannot save.")
        return False
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Generated script saved successfully to: '{filepath}'")
        return True
    except IOError as e:
        print(f"Error saving code to '{filepath}': {e}")
        return False

def execute_generated_script(script_path=GENERATED_SCRIPT_FILENAME):
    """Executes the Python script at the given path using subprocess."""
    if not os.path.exists(script_path):
        print(f"Error: The script to execute '{script_path}' does not exist.")
        return

    print(f"\n--- Executing the generated script: '{script_path}' ---")
    try:
        # Use sys.executable to ensure the script runs with the same Python interpreter
        # that is running this executor script. This is crucial for environment consistency.
        result = subprocess.run(
            [DEFAULT_PYTHON_EXECUTABLE, script_path],
            capture_output=True, 
            text=True, 
            check=True, 
            encoding='utf-8'
        )
        print("--- Script Output ---")
        print(result.stdout)
        if result.stderr:
            print("--- Script Errors (if any) ---")
            print(result.stderr)
        print("--- Script Execution Finished Successfully ---")
    except FileNotFoundError:
        print(f"Error: Python interpreter '{DEFAULT_PYTHON_EXECUTABLE}' not found.")
        print("Ensure Python is installed and its interpreter is correctly located.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script '{script_path}'. It returned a non-zero exit code.")
        print("--- Output (stdout) ---")
        print(e.stdout)
        print("--- Errors (stderr) ---")
        print(e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during script execution: {e}")

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
            print("Failed to save the generated script. Cannot proceed with execution.")
    else:
        print("Failed to get code from Groq API (simulated). Cannot proceed.")

if __name__ == "__main__":
    main()
