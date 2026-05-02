"""
Main Joke Generator module
"""

import requests
import logging
from typing import Dict, Any, Optional, List
import random

# Setup logging
logger = logging.getLogger(__name__)

from .exceptions import (
    JokeAPIError,
    JokeTimeoutError,
    JokeNetworkError,
)


class JokeGenerator:
    """
    A class to generate random jokes using external APIs
    
    Supports multiple joke APIs:
    - JokeAPI (jokeapi.dev)
    - Official Joke API (official-joke-api.appspot.com)
    - Random User Agent for variety
    """

    # API endpoints
    JOKE_API_BASE = "https://v2.jokeapi.dev"
    OFFICIAL_JOKE_API = "https://official-joke-api.appspot.com"
    
    # Request configuration
    DEFAULT_TIMEOUT = 10
    MAX_RETRIES = 3

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize the Joke Generator
        
        Args:
            timeout: Request timeout in seconds (default: 10)
        """
        self.timeout = timeout
        self.session = requests.Session()
        logger.info(f"Joke Generator initialized with timeout: {timeout}s")

    def _make_request(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to the API
        
        Args:
            url: API endpoint URL
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            JokeTimeoutError: If request times out
            JokeAPIError: If API request fails
            JokeNetworkError: If network error occurs
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
            
        except requests.Timeout:
            raise JokeTimeoutError(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise JokeNetworkError("Network connection error")
        except requests.HTTPError as e:
            raise JokeAPIError(f"API error: {e.response.status_code}")
        except Exception as e:
            raise JokeAPIError(f"Request failed: {str(e)}")

    def get_random_joke(self, joke_type: str = "any") -> Dict[str, Any]:
        """
        Get a random joke from JokeAPI
        
        Args:
            joke_type: Type of joke - 'general', 'programming', 'knock-knock', or 'any'
            
        Returns:
            Dictionary containing joke data
            
        Example:
            >>> generator = JokeGenerator()
            >>> joke = generator.get_random_joke()
            >>> print(joke['setup'])
            >>> print(joke['delivery'])
        """
        endpoint = f"{self.JOKE_API_BASE}/joke/{joke_type}"
        
        params = {
            "format": "json",
            "type": "single,twopart",
        }
        
        try:
            response = self.session.get(
                endpoint,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("error"):
                raise JokeAPIError(f"API error: {data.get('message', 'Unknown error')}")
            
            logger.info(f"Successfully fetched joke of type: {joke_type}")
            return data
            
        except requests.Timeout:
            raise JokeTimeoutError(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise JokeNetworkError("Network connection error")
        except requests.HTTPError as e:
            raise JokeAPIError(f"API error: {e.response.status_code}")
        except Exception as e:
            raise JokeAPIError(f"Request failed: {str(e)}")

    def get_official_joke(self) -> Dict[str, Any]:
        """
        Get a random joke from Official Joke API
        
        Returns:
            Dictionary containing joke data
            
        Example:
            >>> joke = generator.get_official_joke()
            >>> print(joke['setup'])
            >>> print(joke['punchline'])
        """
        endpoint = f"{self.OFFICIAL_JOKE_API}/random_joke"
        
        try:
            response = self.session.get(
                endpoint,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            
            logger.info("Successfully fetched joke from Official Joke API")
            return data
            
        except requests.Timeout:
            raise JokeTimeoutError(f"Request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            raise JokeNetworkError("Network connection error")
        except requests.HTTPError as e:
            raise JokeAPIError(f"API error: {e.response.status_code}")
        except Exception as e:
            raise JokeAPIError(f"Request failed: {str(e)}")

    def get_multiple_jokes(self, count: int = 5, source: str = "jokeapi") -> List[Dict[str, Any]]:
        """
        Get multiple random jokes
        
        Args:
            count: Number of jokes to fetch (default: 5, max: 10)
            source: API source - 'jokeapi' or 'official' (default: 'jokeapi')
            
        Returns:
            List of joke dictionaries
        """
        if count > 10:
            logger.warning(f"Limiting jokes to 10 (requested: {count})")
            count = 10
        
        jokes = []
        
        try:
            for i in range(count):
                if source == "official":
                    joke = self.get_official_joke()
                else:
                    joke = self.get_random_joke()
                jokes.append(joke)
            
            logger.info(f"Successfully fetched {count} jokes")
            return jokes
            
        except Exception as e:
            logger.error(f"Error fetching jokes: {str(e)}")
            raise

    def get_joke_by_type(self, joke_type: str) -> Dict[str, Any]:
        """
        Get a joke by specific type
        
        Args:
            joke_type: Type of joke - 'general' or 'programming'
            
        Returns:
            Dictionary containing joke data
            
        Raises:
            JokeAPIError: If invalid joke type is provided
        """
        valid_types = ["general", "programming", "knock-knock", "any"]
        
        if joke_type not in valid_types:
            raise JokeAPIError(f"Invalid joke type. Valid types: {', '.join(valid_types)}")
        
        return self.get_random_joke(joke_type=joke_type)

    def format_joke(self, joke: Dict[str, Any]) -> str:
        """
        Format joke data into readable string
        
        Args:
            joke: Joke dictionary
            
        Returns:
            Formatted joke string
        """
        if "punchline" in joke:
            # Official Joke API format
            return f"{joke['setup']}\n{joke['punchline']}"
        elif "delivery" in joke:
            # JokeAPI two-part format
            return f"{joke['setup']}\n{joke['delivery']}"
        else:
            # JokeAPI single joke format
            return joke.get("joke", "No joke found")

    def close(self) -> None:
        """
        Close the session
        """
        self.session.close()
        logger.info("Joke Generator session closed")
