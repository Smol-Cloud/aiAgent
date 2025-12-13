import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    # Set directory display name:
    if directory == ".":
        directory_display_name = "current"
    else:
        directory_display_name = f"'{directory}'"

    # Check if valid subdirectory
    if not is_subdirectory(working_directory, directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Calculate the full path
    full_path = os.path.join(working_directory, directory)
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    # List directory contents
    directory_contents = os.listdir(full_path)

    lines = [f"Result for {directory_display_name} directory:\n"]

    # Generate print directory content string
    for content in directory_contents:
        # Generate absolute path
        abs_path_content = os.path.abspath(os.path.join(full_path, content))

        # Get file size
        content_size = os.path.getsize(abs_path_content)

        # Determine whether content is directory
        is_dir = os.path.isdir(abs_path_content)

        lines.append(f"  - {content}: file_size={content_size} bytes, is_dir={is_dir}\n")
    
    return "".join(lines)

# Get absolute paths for parent and child
def get_abs_path(parent, child):
    return os.path.abspath(parent), os.path.abspath(os.path.join(parent, child))

# Check if child is subdirectory of parent
def is_subdirectory(parent, child):
    parent_abs, child_abs = get_abs_path(parent, child)
    return os.path.commonpath([parent_abs]) == os.path.commonpath([parent_abs, child_abs])

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)