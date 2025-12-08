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

    # Get a response from client
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    )
    print(response.text)


if __name__ == "__main__":
    main()
