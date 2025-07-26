#!/usr/bin/env python3
"""
A robust client for interacting with the SearXNG meta-search engine.
"""

import logging
from datetime import datetime
from typing import Dict, Any

import requests

from .config import SearchConfig
from .exceptions import NetworkError, APIError
from .models import SearchResult, SearchResponse


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
                raise APIError("Empty response from SearXNG")
            
            try:
                data = response.json()
            except ValueError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                raise APIError(f"Invalid JSON response from SearXNG: {e}")
            
            return data
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout after {self.config.timeout} seconds")
            raise NetworkError("Request to SearXNG timed out")
        
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Failed to connect to SearXNG at {self.config.base_url}")
            raise NetworkError(f"Cannot connect to SearXNG at {self.config.base_url}")
        
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            if response.status_code == 403:
                raise APIError("Access forbidden - check if JSON format is enabled")
            elif response.status_code == 429:
                raise APIError("Rate limit exceeded - try again later")
            else:
                raise NetworkError(f"HTTP {response.status_code}: {e}")
    
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