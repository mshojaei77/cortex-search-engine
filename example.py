#!/usr/bin/env python3
"""
Example script demonstrating how to use the search_engine library directly.
"""

import logging
from search_engine import SearchEngineManager, display_results, SearXNGException

def run_example_search():
    """
    Runs a quick search for "latest python features" and displays the results.
    """
    print("🚀 Running example search...")
    
    try:
        # 1. Create a SearchEngineManager instance
        # This automatically picks up configuration from environment variables
        # or defaults to http://localhost:8888.
        manager = SearchEngineManager()

        # 2. Perform a quick search
        # This is a simplified method for getting a list of results.
        query = "latest python features"
        print(f"🔍 Searching for: \"{query}\"")
        results = manager.quick_search(query)

        # 3. Display the results in a formatted way
        # The display_results utility provides a clean console output.
        display_results(results, title=f"Results for '{query}'")

    except SearXNGException as e:
        logging.error(f"An error occurred during the search: {e}")
        print(f"\n❌ Search failed. Is the SearXNG Docker container running?")
        print("   You can start it by running: python setup.py")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        print("\n❌ An unexpected error occurred. Please check the logs.")


if __name__ == "__main__":
    # Configure logging to show info-level messages
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    run_example_search() 