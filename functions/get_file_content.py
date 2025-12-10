import os
#import config

def get_file_content(working_directory, file_path):
    # Check if valid 
    if not is_subdirectory(working_directory, file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Calculate the full path
    full_path = os.path.join(working_directory, file_path)

    # Check if file
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    with open(full_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
    return file_content_string

# Get absolute paths for parent and child
def get_abs_path(parent, child):
    return os.path.abspath(parent), os.path.abspath(os.path.join(parent, child))

# Check if child is present in parent dir
def is_subdirectory(parent, child):
    parent_abs, child_abs = get_abs_path(parent, child)
    return os.path.commonpath([parent_abs]) == os.path.commonpath([parent_abs, child_abs])

