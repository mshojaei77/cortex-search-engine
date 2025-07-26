#!/usr/bin/env python3
"""
Utility functions for the search engine client.
"""

from typing import List, Dict


def display_results(results: List[Dict[str, str]], title: str = "Search Results"):
    """
    Display search results in a formatted way.
    
    Args:
        results: List of search result dictionaries
        title: Title to display above results
    """
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    
    if not results:
        print("No results found.")
        return
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        if result.get('snippet'):
            print(f"   Snippet: {result['snippet']}")
        if result.get('engines'):
            print(f"   Sources: {result['engines']}")
        print("-" * 60)
    
    print(f"\nTotal results: {len(results)}") 