#!/usr/bin/env python3
"""
Configuration for the SearXNG search client.
"""

from typing import List, Optional
from dataclasses import dataclass, field


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