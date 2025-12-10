import os
#import config

def write_file(working_directory, file_path, content):
    # Check if valid 
    if not is_subdirectory(working_directory, file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Calculate the full path
    full_path = os.path.join(working_directory, file_path)

    # Make any directories that do not yet exist
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Write to the file
    with open(full_path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

# Get absolute paths for parent and child
def get_abs_path(parent, child):
    return os.path.abspath(parent), os.path.abspath(os.path.join(parent, child))

# Check if child is present in parent dir
def is_subdirectory(parent, child):
    parent_abs, child_abs = get_abs_path(parent, child)
    return os.path.commonpath([parent_abs]) == os.path.commonpath([parent_abs, child_abs])