#!/usr/bin/env python3
"""
SearXNG Meta-Search Engine Client

A robust, production-ready Python client for the SearXNG meta-search engine.
"""

# Configure logging
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up a default logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Public API for the search_engine package
from .client import SearXNGClient
from .config import SearchConfig
from .manager import SearchEngineManager
from .models import SearchResult, SearchResponse
from .utils import display_results
from .exceptions import SearXNGException, NetworkError, APIError, InvalidConfigurationError

__all__ = [
    "SearXNGClient",
    "SearchConfig",
    "SearchEngineManager",
    "SearchResult",
    "SearchResponse",
    "display_results",
    "SearXNGException",
    "NetworkError",
    "APIError",
    "InvalidConfigurationError",
]

__version__ = "1.0.0" 