#!/usr/bin/env python3
"""
Custom exceptions for the SearXNG client.
"""


class SearXNGException(Exception):
    """Base exception for all SearXNG client errors."""
    pass


class NetworkError(SearXNGException):
    """Raised for network-related errors (e.g., connection, timeout)."""
    pass


class APIError(SearXNGException):
    """Raised for API-specific errors (e.g., invalid response, rate limits)."""
    pass


class InvalidConfigurationError(SearXNGException):
    """Raised for invalid configuration parameters."""
    pass 