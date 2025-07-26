import os
import json
from typing import List, Dict, Any

from openai import OpenAI
from dotenv import load_dotenv

from search_engine import SearchEngineManager, SearXNGException

# Load environment variables from .env file
load_dotenv(encoding='utf-8-sig')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize search engine manager
search_manager = SearchEngineManager()


def search_web(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a web search using the SearXNG engine.

    Args:
        query: The search query.
        max_results: The maximum number of results to return.

    Returns:
        A list of search result dictionaries.
    """
    try:
        results = search_manager.quick_search(query, max_results=max_results)
        return results
    except SearXNGException as e:
        print(f"ERROR: Search failed: {e}")
        return []


# Define the search tool for the OpenAI model
search_tool = {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Look up real-time information on the public web.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to use. Be specific and descriptive."
                },
                "max_results": {
                    "type": "integer",
                    "description": "The maximum number of search results to return.",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
}


def run_agent(user_input: str) -> str:
    """
    Run the web search agent for a single turn.

    Args:
        user_input: The user's query.

    Returns:
        The agent's response.
    """
    system_msg = {
        "role": "system",
        "content": "You are a helpful search assistant. When you need up-to-date information, use the search_web tool."
    }
    
    messages = [system_msg, {"role": "user", "content": user_input}]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=[search_tool],
            tool_choice="auto"
        )
        
        msg = response.choices[0].message

        if msg.tool_calls:
            call = msg.tool_calls[0]
            if call.function.name == "search_web":
                args = json.loads(call.function.arguments)
                results = search_web(**args)
                
                messages.append(msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": "search_web",
                    "content": json.dumps(results, indent=2)
                })
                
                final_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                return final_response.choices[0].message.content
        
        return msg.content

    except Exception as e:
        return f"ERROR: An unexpected error occurred: {e}"


def main():
    """
    Main function to run the web search assistant.
    """
    print("Web Search Assistant (type 'exit' to quit)")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting...")
                break
            
            if not user_input.strip():
                continue

            response = run_agent(user_input)
            print(f"Assistant: {response}")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"ERROR: A critical error occurred in main loop: {e}")
            import traceback
            traceback.print_exc()
            break


if __name__ == "__main__":
    main()
