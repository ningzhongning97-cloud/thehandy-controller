"""
Custom exceptions for The Handy Controller
"""


class HandyException(Exception):
    """Base exception for The Handy Controller"""
    pass


class HandyConnectionError(HandyException):
    """Raised when connection to device fails"""
    pass


class HandyAPIError(HandyException):
    """Raised when API request fails"""
    pass


class HandyTimeoutError(HandyException):
    """Raised when request times out"""
    pass


class HandyDeviceError(HandyException):
    """Raised when device returns an error"""
    pass
