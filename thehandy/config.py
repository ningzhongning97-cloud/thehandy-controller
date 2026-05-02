"""
Configuration management for The Handy Controller
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for The Handy Controller"""

    # API Configuration
    API_BASE_URL = os.getenv("HANDY_API_URL", "https://www.handyfeeling.com/api/v1")
    CONNECTION_KEY = os.getenv("HANDY_CONNECTION_KEY", "")
    
    # Request Configuration
    REQUEST_TIMEOUT = int(os.getenv("HANDY_REQUEST_TIMEOUT", "10"))
    MAX_RETRIES = int(os.getenv("HANDY_MAX_RETRIES", "3"))
    
    # Device Configuration
    DEVICE_ID = os.getenv("HANDY_DEVICE_ID", "")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("HANDY_LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("HANDY_LOG_FILE", "thehandy.log")


def get_config():
    """Get configuration instance"""
    return Config()
