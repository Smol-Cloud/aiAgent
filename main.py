import os
from dotenv import load_dotenv
from google import genai

def main():
    print("Hello from aiagent!")
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print("API Key loaded successfully.")
    else:
        raise RuntimeError("API Key not found. Please set GEMINI_API_KEY in your .env file.")
    # Create a new instance of Gemini Client
    client = genai.Client(api_key=api_key)

    # Define a prompt to be passed to the AI Agent
    prompt = 'Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'

    # Get a response from client
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=prompt
    )

    # Verify that the usage metadata property is not None.
    if not(response.usage_metadata):
        raise RuntimeError("Gemini API call error")

    # Extract the prompt token count and the candidate token count
    prompt_token_count = response.usage_metadata.prompt_token_count
    candidate_token_count = response.usage_metadata.candidates_token_count

    # Print out response:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {candidate_token_count}")
    print(f"Response:")
    print(response.text)

if __name__ == "__main__":
    main()
