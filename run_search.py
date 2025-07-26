#!/usr/bin/env python3
"""
Simple AI News Search Script

A straightforward script to search for AI news using the SearXNG search engine.
"""

from search_engine import SearchEngineManager, display_results


def search_ai_news_2025():
    """Search for AI news 2025 and display results."""
    try:
        print("🤖 Searching for AI News 2025...")
        print("=" * 40)
        
        # Create search manager
        manager = SearchEngineManager()
        
        # Perform the search
        results = manager.search_ai_news("2025", max_results=15)
        
        # Display results
        display_results(results, "🗞️ AI News 2025")
        
        if results:
            print(f"\n📈 Summary:")
            print(f"   • Found {len(results)} AI news articles")
            print(f"   • Search engines used: Multiple meta-search sources")
            print(f"   • Focus: Artificial Intelligence developments in 2025")
        
        return True
        
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False


if __name__ == "__main__":
    search_ai_news_2025() 