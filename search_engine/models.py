#!/usr/bin/env python3
"""
Data models for the SearXNG search engine client.
"""

from typing import List, Optional
from dataclasses import dataclass, field


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