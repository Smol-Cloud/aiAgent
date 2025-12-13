import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):

    # Check if valid 
    if not is_subdirectory(working_directory, file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Calculate the full path
    full_path = os.path.join(working_directory, file_path)

    # Check if file
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    
    # Check if python file
    if not os.path.splitext(full_path)[1] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # Run python file
        script_output = subprocess.run(["python", f"{full_path}"] + args, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return "Error: The script timed out."
    except Exception as e:
        return f"Error running subprocess: {e}"
    
    # Init return text
    return_text = ""

    # If non-zero return code:
    if script_output.returncode != 0: 
        return_text += f"\nProcess exited with code {script_output.returncode}"

    # Check if no output:
    if not(script_output.stdout):
        return_text += "\nNo output produced"

    # Include STDOUT
    return_text += f"\nSTDOUT: {script_output.stdout}"

    # Include STDERR
    return_text += f"\nSTDERR: {script_output.stderr}"

    return return_text

# Get absolute paths for parent and child
def get_abs_path(parent, child):
    return os.path.abspath(parent), os.path.abspath(os.path.join(parent, child))

# Check if child is present in parent dir
def is_subdirectory(parent, child):
    parent_abs, child_abs = get_abs_path(parent, child)
    return os.path.commonpath([parent_abs]) == os.path.commonpath([parent_abs, child_abs])

