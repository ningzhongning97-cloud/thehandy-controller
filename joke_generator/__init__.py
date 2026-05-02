"""
Random Joke Generator - A Python library for generating random jokes

Version: 1.0.0
"""

from .generator import JokeGenerator
from .exceptions import (
    JokeException,
    JokeAPIError,
    JokeTimeoutError,
    JokeNetworkError,
)

__version__ = "1.0.0"
__all__ = [
    "JokeGenerator",
    "JokeException",
    "JokeAPIError",
    "JokeTimeoutError",
    "JokeNetworkError",
]
