import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from search_engine import (
    SearchEngineManager, 
    display_results,
    SearXNGException
)


def main():
    """Main function to demonstrate the SearXNG client functionality."""
    try:
        print("SearXNG Meta-Search Engine Client")
        
        # Initialize search engine manager
        manager = SearchEngineManager()
        
        # Check health status
        with manager.create_client() as client:
            health = client.get_health_status()
            if health['status'] != 'healthy':
                print(f"ERROR: SearXNG is unhealthy: {health.get('error', 'Unknown error')}")
                sys.exit(1)
            print(f"SUCCESS: SearXNG is healthy")
        
        # AI news search for 2025
        ai_results = manager.search_ai_news("2025", max_results=10)
        display_results(ai_results, "AI News 2025")
        
        # General search
        general_results = manager.quick_search("machine learning trends 2025", max_results=5)
        display_results(general_results, "ML Trends 2025")
        
        # Advanced search
        with manager.create_client(
            engines=['google', 'bing', 'duckduckgo'],
            time_range='month'
        ) as client:
            response = client.search("artificial intelligence breakthroughs")
            
            simplified_results = [
                {
                    'title': result.title,
                    'url': result.url,
                    'snippet': result.content[:200] + "..." if len(result.content) > 200 else result.content,
                    'engines': ', '.join(result.engines)
                }
                for result in response.results[:3]
            ]
            display_results(simplified_results, "AI Breakthroughs")
        
        print("SUCCESS: All searches completed successfully!")
        
    except SearXNGException as e:
        print(f"ERROR: Search error: {e}")
    except KeyboardInterrupt:
        print("INTERRUPTED: Search interrupted")
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")


if __name__ == "__main__":
    main()