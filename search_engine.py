#!/usr/bin/env python3
"""
SearXNG Meta-Search Engine Client

A robust, production-ready Python client for SearXNG meta-search engine
that follows SOLID principles and provides comprehensive search functionality.

Author: Personal Search Engine Project
Date: 2025
"""

import os
import logging
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@dataclass
class SearchResult:
    """Model for individual search result."""
    
    title: str
    url: str
    content: str = ""
    engines: List[str] = field(default_factory=list)
    category: str = "general"
    publishedDate: Optional[str] = None


@dataclass
class SearchResponse:
    """Model for complete search response."""
    
    query: str
    results: List[SearchResult] = field(default_factory=list)
    total_results: int = 0
    search_time: float = 0.0
    engines_used: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class SearchConfig:
    """Configuration for search parameters."""
    
    base_url: str = field(default="http://localhost:8888")
    timeout: int = field(default=30)
    max_results: int = field(default=10)
    language: str = field(default="en")
    safe_search: int = field(default=0)  # 0=off, 1=moderate, 2=strict
    time_range: Optional[str] = field(default=None)  # day, month, year
    categories: List[str] = field(default_factory=lambda: ["general"])
    engines: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.base_url.startswith(('http://', 'https://')):
            raise ValueError("Base URL must start with http:// or https://")
        
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        
        if self.max_results <= 0:
            raise ValueError("Max results must be positive")
        
        if self.safe_search not in [0, 1, 2]:
            raise ValueError("Safe search must be 0, 1, or 2")


class SearXNGClient:
    """
    A robust client for interacting with SearXNG meta-search engine.
    
    This class provides a clean interface for performing searches,
    handling errors, and processing results from SearXNG instances.
    """
    
    def __init__(self, config: SearchConfig):
        """
        Initialize the SearXNG client.
        
        Args:
            config: SearchConfig object with search parameters
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'SearXNG-Python-Client/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    
    def _build_search_params(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Build search parameters for the API request.
        
        Args:
            query: Search query string
            **kwargs: Additional search parameters
            
        Returns:
            Dictionary of search parameters
        """
        params = {
            'q': query,
            'format': 'json',
            'language': self.config.language,
            'safesearch': self.config.safe_search,
        }
        
        # Add optional parameters
        if self.config.time_range:
            params['time_range'] = self.config.time_range
        
        if self.config.categories:
            params['categories'] = ','.join(self.config.categories)
        
        if self.config.engines:
            params['engines'] = ','.join(self.config.engines)
        
        # Override with any additional parameters
        params.update(kwargs)
        
        return params
    
    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make HTTP request to SearXNG API.
        
        Args:
            params: Search parameters
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.RequestException: For HTTP-related errors
            ValueError: For invalid responses
        """
        try:
            self.logger.info(f"Making search request with query: {params.get('q', 'N/A')}")
            
            response = self.session.get(
                f"{self.config.base_url}/search",
                params=params,
                timeout=self.config.timeout
            )
            
            response.raise_for_status()
            
            if not response.text.strip():
                raise ValueError("Empty response from SearXNG")
            
            try:
                data = response.json()
            except ValueError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                raise ValueError(f"Invalid JSON response from SearXNG: {e}")
            
            return data
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout after {self.config.timeout} seconds")
            raise requests.RequestException("Request to SearXNG timed out")
        
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Failed to connect to SearXNG at {self.config.base_url}")
            raise requests.RequestException(f"Cannot connect to SearXNG at {self.config.base_url}")
        
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            if response.status_code == 403:
                raise requests.RequestException("Access forbidden - check if JSON format is enabled")
            elif response.status_code == 429:
                raise requests.RequestException("Rate limit exceeded - try again later")
            else:
                raise requests.RequestException(f"HTTP {response.status_code}: {e}")
    
    def _parse_results(self, data: Dict[str, Any], query: str, search_time: float) -> SearchResponse:
        """
        Parse raw SearXNG response into SearchResponse model.
        
        Args:
            data: Raw response data from SearXNG
            query: Original search query
            search_time: Time taken for the search
            
        Returns:
            SearchResponse object
        """
        results = []
        
        for item in data.get('results', [])[:self.config.max_results]:
            try:
                url = item.get('url', '')
                if url and not url.startswith(('http://', 'https://')):
                    self.logger.warning(f"Skipping result with invalid URL: {url}")
                    continue

                result = SearchResult(
                    title=item.get('title', 'No title'),
                    url=url,
                    content=item.get('content', ''),
                    engines=item.get('engines', []),
                    category=item.get('category', 'general'),
                    publishedDate=item.get('publishedDate')
                )
                results.append(result)
            except Exception as e:
                self.logger.warning(f"Failed to parse result: {e}")
                continue
        
        # Extract engine information
        engines_used = list(set(
            engine for result in results for engine in result.engines
        ))
        
        return SearchResponse(
            query=query,
            results=results,
            total_results=len(results),
            search_time=search_time,
            engines_used=engines_used,
            suggestions=data.get('suggestions', [])
        )
    
    def search(self, query: str, **kwargs) -> SearchResponse:
        """
        Perform a search query using SearXNG.
        
        Args:
            query: Search query string
            **kwargs: Additional search parameters to override defaults
            
        Returns:
            SearchResponse object containing results
            
        Raises:
            ValueError: For invalid queries or parameters
            requests.RequestException: For network/API errors
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")
        
        start_time = datetime.now()
        
        try:
            params = self._build_search_params(query.strip(), **kwargs)
            data = self._make_request(params)
            
            search_time = (datetime.now() - start_time).total_seconds()
            
            return self._parse_results(data, query, search_time)
            
        except Exception as e:
            self.logger.error(f"Search failed for query '{query}': {e}")
            raise
    
    def search_news(self, query: str, **kwargs) -> SearchResponse:
        """
        Perform a news-specific search.
        
        Args:
            query: Search query string
            **kwargs: Additional search parameters
            
        Returns:
            SearchResponse object containing news results
        """
        news_params = {
            'categories': 'news',
            'time_range': kwargs.pop('time_range', 'year')
        }
        news_params.update(kwargs)
        
        return self.search(query, **news_params)
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Check the health status of the SearXNG instance.
        
        Returns:
            Dictionary with health status information
        """
        try:
            response = self.session.get(
                f"{self.config.base_url}/config",
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            return {
                'status': 'healthy',
                'url': self.config.base_url,
                'response_time': response.elapsed.total_seconds(),
                'config': response.json()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'url': self.config.base_url,
                'error': str(e)
            }
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


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


if __name__ == "__main__":
    """
    Main function to test the SearXNG client with AI news search.
    This demonstrates the functionality and serves as a usage example.
    """
    try:
        print("🔍 SearXNG Meta-Search Engine Client")
        print("=====================================")
        
        # Initialize search engine manager
        manager = SearchEngineManager()
        
        # Check health status first
        print("\n📊 Checking SearXNG health status...")
        with manager.create_client() as client:
            health = client.get_health_status()
            if health['status'] == 'healthy':
                print(f"✅ SearXNG is healthy at {health['url']}")
                print(f"   Response time: {health['response_time']:.2f}s")
            else:
                print(f"❌ SearXNG is unhealthy: {health.get('error', 'Unknown error')}")
                print("   Please ensure SearXNG is running and accessible")
                exit(1)
        
        # Perform AI news search for 2025
        print("\n🤖 Searching for AI news 2025...")
        ai_results = manager.search_ai_news("2025", max_results=10)
        display_results(ai_results, "AI News 2025")
        
        # Perform a general search example
        print("\n🔍 Performing general search example...")
        general_results = manager.quick_search("machine learning trends 2025", max_results=5)
        display_results(general_results, "Machine Learning Trends 2025")
        
        # Demonstrate advanced search with custom parameters
        print("\n🎯 Advanced search with custom parameters...")
        with manager.create_client(
            engines=['google', 'bing', 'duckduckgo'],
            time_range='month'
        ) as client:
            response = client.search("artificial intelligence breakthroughs")
            
            print(f"\nSearch completed in {response.search_time:.2f} seconds")
            print(f"Engines used: {', '.join(response.engines_used)}")
            print(f"Total results: {response.total_results}")
            
            # Display top 3 results
            display_results([
                {
                    'title': result.title,
                    'url': result.url,
                    'snippet': result.content[:200] + "..." if len(result.content) > 200 else result.content,
                    'engines': ', '.join(result.engines)
                }
                for result in response.results[:3]
            ], "AI Breakthroughs (Advanced Search)")
        
        print("\n✅ All searches completed successfully!")
        print("\n💡 Tips:")
        print("   - Ensure SearXNG is running: docker-compose up -d")
        print("   - Access web interface: http://localhost:8888")
        print("   - Customize search parameters in SearchConfig")
        print("   - Use environment variables for configuration")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Search interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if SearXNG is running: docker-compose ps")
        print("   2. Verify JSON format is enabled in settings.yml")
        print("   3. Check network connectivity to SearXNG")
        print("   4. Review logs: docker-compose logs searxng") 