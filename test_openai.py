import os
from openai import OpenAI
from dotenv import load_dotenv

def check_api_key_and_balance():
    """
    Checks for the presence of an OpenAI API key in the environment variables,
    and validates it by sending a simple request to the API.
    """
    print("--- OpenAI API Key and Balance Test ---")

    # Load environment variables from .env file
    load_dotenv(encoding="utf-8-sig")
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not found.")
        print("Please create a .env file in the root directory and add your key:")
        print("OPENAI_API_KEY='your-api-key-here'")
        return

    print("✔ OPENAI_API_KEY found.")

    try:
        # Initialize OpenAI client with the API key
        client = OpenAI(api_key=api_key)
        print("✔ OpenAI client initialized successfully.")

        # Send a simple request to test the key and model access
        print("Sending a test request to the gpt-4.1-nano model...")
        response = client.chat.completions.create(
            model="gpt-4.1-nano",  # A known, cost-effective model
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        print(response)
        print("✔ Test request successful.")
        print("✔ Your API key is valid and has sufficient credit.")
        print("--- Test Complete ---")

    except Exception as e:
        print("\nERROR: An error occurred during the API test.")
        if "Incorrect API key provided" in str(e):
            print("The provided API key is incorrect. Please check your .env file.")
        elif "You exceeded your current quota" in str(e):
            print("You have exceeded your OpenAI API quota. Please check your billing details.")
        else:
            print(f"An unexpected error occurred: {e}")
        print("--- Test Failed ---")

if __name__ == "__main__":
    check_api_key_and_balance() 