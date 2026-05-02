"""
The Handy Controller - Python library for controlling The Handy device

Version: 0.1.0
"""

from .client import HandyController
from .exceptions import (
    HandyException,
    HandyConnectionError,
    HandyAPIError,
    HandyTimeoutError,
    HandyDeviceError,
)

__version__ = "0.1.0"
__all__ = [
    "HandyController",
    "HandyException",
    "HandyConnectionError",
    "HandyAPIError",
    "HandyTimeoutError",
    "HandyDeviceError",
]
