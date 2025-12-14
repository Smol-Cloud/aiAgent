import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_files import schema_write_file
from functions.call_function import call_function

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    print("Hello from aiagent!")
    print(f"System Prompt: {SYSTEM_PROMPT}")

    # Generate list of possible tools
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
    )

    # Parse arguments from commandline
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.prompt`

    # Create a new list of types.Content, and set the user's prompt as the only message (for now):
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

    # Grab API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print("API Key loaded successfully.")
    else:
        raise RuntimeError("API Key not found. Please set GEMINI_API_KEY in your .env file.")
    
    # Create a new instance of Gemini Client
    client = genai.Client(api_key=api_key)

    # Get a response from client
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[available_functions])
    )

    # Verify that the usage metadata property is not None.
    if not(response.usage_metadata):
        raise RuntimeError("Gemini API call error")

    # Extract the prompt token count and the candidate token count
    prompt_token_count = response.usage_metadata.prompt_token_count
    candidate_token_count = response.usage_metadata.candidates_token_count

    # Print out response:
    # Verbose case:
    if args.verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidate_token_count}")
    print(f"Response:")

    # Initialise a list to hold function responses
    function_responses = list()

    # Check if a function call was returned
    if response.function_calls:
        for function_call_part in response.function_calls:
            #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_result = call_function(function_call_part, verbose=args.verbose)

            if not(function_call_result.parts[0].function_response.response):
                raise Exception("Function call failed to return")
            
            function_responses.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else: 
        print(response.text)

if __name__ == "__main__":
    main()
