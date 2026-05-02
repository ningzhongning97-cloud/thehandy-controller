"""
Custom exceptions for Joke Generator
"""


class JokeException(Exception):
    """Base exception for Joke Generator"""
    pass


class JokeAPIError(JokeException):
    """Raised when API request fails"""
    pass


class JokeTimeoutError(JokeException):
    """Raised when request times out"""
    pass


class JokeNetworkError(JokeException):
    """Raised when network error occurs"""
    pass
