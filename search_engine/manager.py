#!/usr/bin/env python3
"""
High-level manager for search operations.
"""

import os
import logging
from typing import List, Dict

from .client import SearXNGClient
from .config import SearchConfig


class SearchEngineManager:
    """
    High-level manager for search operations.
    
    This class provides a simplified interface for common search tasks
    and manages multiple search configurations.
    """
    
    def __init__(self, base_url: str = None):
        """
        Initialize the search engine manager.
        
        Args:
            base_url: Base URL for SearXNG instance (defaults to env var or localhost)
        """
        self.base_url = base_url or os.getenv('SEARXNG_URL', 'http://localhost:8888')
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def create_client(self, **config_overrides) -> SearXNGClient:
        """
        Create a SearXNG client with custom configuration.
        
        Args:
            **config_overrides: Configuration parameters to override
            
        Returns:
            Configured SearXNGClient instance
        """
        config_params = {
            'base_url': self.base_url,
            'timeout': int(os.getenv('SEARXNG_TIMEOUT', 30)),
            'max_results': int(os.getenv('SEARXNG_MAX_RESULTS', 10)),
            'language': os.getenv('SEARXNG_LANGUAGE', 'en'),
        }
        config_params.update(config_overrides)
        
        config = SearchConfig(**config_params)
        return SearXNGClient(config)
    
    def quick_search(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Perform a quick search and return simplified results.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of simplified result dictionaries
        """
        with self.create_client(max_results=max_results) as client:
            response = client.search(query)
            
            return [
                {
                    'title': result.title,
                    'url': result.url,
                    'snippet': result.content[:200] + "..." if len(result.content) > 200 else result.content,
                    'engines': ', '.join(result.engines)
                }
                for result in response.results
            ]
    
    def search_ai_news(self, year: str = "2025", max_results: int = 15) -> List[Dict[str, str]]:
        """
        Search for AI news for a specific year.
        
        Args:
            year: Year to search for (default: 2025)
            max_results: Maximum number of results
            
        Returns:
            List of AI news results
        """
        query = f"AI news {year} artificial intelligence"
        
        with self.create_client(max_results=max_results) as client:
            response = client.search_news(query, time_range='year')
            
            return [
                {
                    'title': result.title,
                    'url': result.url,
                    'snippet': result.content[:300] + "..." if len(result.content) > 300 else result.content,
                    'engines': ', '.join(result.engines),
                    'category': result.category
                }
                for result in response.results
            ] 