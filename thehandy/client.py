"""
Main API client for The Handy Controller
"""

import requests
import logging
from typing import Dict, Any, Optional
from .config import get_config
from .exceptions import (
    HandyConnectionError,
    HandyAPIError,
    HandyTimeoutError,
    HandyDeviceError,
)

# Setup logging
logger = logging.getLogger(__name__)


class HandyController:
    """Main controller class for interacting with The Handy device"""

    def __init__(self, connection_key: Optional[str] = None):
        """
        Initialize The Handy Controller

        Args:
            connection_key: Connection key for the device. If not provided, will use env variable
        """
        self.config = get_config()
        self.connection_key = connection_key or self.config.CONNECTION_KEY
        
        if not self.connection_key:
            raise HandyConnectionError("Connection key is required. Set HANDY_CONNECTION_KEY environment variable.")
        
        self.base_url = self.config.API_BASE_URL
        self.timeout = self.config.REQUEST_TIMEOUT
        self.session = requests.Session()
        self._is_connected = False
        self._device_info = None

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        return {
            "Content-Type": "application/json",
            "X-Connection-Key": self.connection_key,
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to The Handy API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dictionary

        Raises:
            HandyTimeoutError: If request times out
            HandyAPIError: If API request fails
            HandyDeviceError: If device returns an error
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )

            if response.status_code == 200 or response.status_code == 201:
                return response.json() if response.text else {}
            elif response.status_code == 401:
                raise HandyConnectionError("Invalid connection key")
            elif response.status_code == 404:
                raise HandyAPIError(f"Endpoint not found: {endpoint}")
            else:
                raise HandyDeviceError(f"Device error: {response.status_code} - {response.text}")

        except requests.Timeout:
            raise HandyTimeoutError(f"Request timed out after {self.timeout} seconds")
        except requests.RequestException as e:
            raise HandyAPIError(f"Request failed: {str(e)}")

    def connect(self) -> bool:
        """
        Connect to the device

        Returns:
            True if connection successful
        """
        try:
            self._device_info = self.get_device_info()
            self._is_connected = True
            logger.info(f"Connected to device: {self._device_info}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {str(e)}")
            self._is_connected = False
            raise

    def disconnect(self) -> bool:
        """
        Disconnect from the device

        Returns:
            True if disconnection successful
        """
        try:
            self.session.close()
            self._is_connected = False
            logger.info("Disconnected from device")
            return True
        except Exception as e:
            logger.error(f"Failed to disconnect: {str(e)}")
            raise

    def is_connected(self) -> bool:
        """
        Check if connected to device

        Returns:
            True if connected, False otherwise
        """
        return self._is_connected

    def get_device_info(self) -> Dict[str, Any]:
        """
        Get device information

        Returns:
            Device information dictionary
        """
        return self._make_request("GET", "/device")

    def get_status(self) -> Dict[str, Any]:
        """
        Get current device status

        Returns:
            Device status dictionary
        """
        return self._make_request("GET", "/status")

    def set_speed(self, speed: int) -> Dict[str, Any]:
        """
        Set device speed

        Args:
            speed: Speed value (0-100)

        Returns:
            Response data
        """
        if not 0 <= speed <= 100:
            raise ValueError("Speed must be between 0 and 100")
        
        return self._make_request("PUT", "/speed", data={"speed": speed})

    def set_position(self, position: int) -> Dict[str, Any]:
        """
        Set device position

        Args:
            position: Position value (0-100)

        Returns:
            Response data
        """
        if not 0 <= position <= 100:
            raise ValueError("Position must be between 0 and 100")
        
        return self._make_request("PUT", "/position", data={"position": position})

    def stop(self) -> Dict[str, Any]:
        """
        Stop the device

        Returns:
            Response data
        """
        return self._make_request("POST", "/stop")

    def play_script(self, script_id: str) -> Dict[str, Any]:
        """
        Play a script on the device

        Args:
            script_id: ID of the script to play

        Returns:
            Response data
        """
        return self._make_request("POST", f"/scripts/{script_id}/play")

    def pause_script(self) -> Dict[str, Any]:
        """
        Pause current script

        Returns:
            Response data
        """
        return self._make_request("POST", "/scripts/pause")

    def resume_script(self) -> Dict[str, Any]:
        """
        Resume paused script

        Returns:
            Response data
        """
        return self._make_request("POST", "/scripts/resume")

    def get_scripts(self) -> Dict[str, Any]:
        """
        Get list of available scripts

        Returns:
            List of scripts
        """
        return self._make_request("GET", "/scripts")
