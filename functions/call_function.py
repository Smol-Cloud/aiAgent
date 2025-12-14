from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_files import write_file



def call_function(function_call_part, verbose=False):
    # function_call_part is a types.FunctionCall object that has, most importantly:
    # A name property (the name of the function, a string)
    # An args property (a dict of named arguments to the function)

    # Create a dictionary that maps name -> function
    functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    function_name = function_call_part.name

    if not(function_name in functions):
        # If function name is invalid, return a types.Content object that explains the error:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    completed_args = {**function_call_part.args, "working_directory": "./calculator"}

    # If verbose is specified, print function call name and arguments
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_result = functions[function_name](**completed_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )





