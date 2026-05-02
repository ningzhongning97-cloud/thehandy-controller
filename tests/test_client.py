"""
Unit tests for The Handy Controller
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from thehandy import HandyController
from thehandy.exceptions import (
    HandyConnectionError,
    HandyAPIError,
    HandyTimeoutError,
    HandyDeviceError,
)


class TestHandyController(unittest.TestCase):
    """Test cases for HandyController"""

    def setUp(self):
        """Set up test fixtures"""
        os.environ['HANDY_CONNECTION_KEY'] = 'test_key_12345'

    def tearDown(self):
        """Clean up after tests"""
        if 'HANDY_CONNECTION_KEY' in os.environ:
            del os.environ['HANDY_CONNECTION_KEY']

    def test_init_with_connection_key(self):
        """Test controller initialization with connection key"""
        controller = HandyController(connection_key='test_key')
        self.assertEqual(controller.connection_key, 'test_key')
        self.assertFalse(controller.is_connected())

    def test_init_without_connection_key(self):
        """Test controller initialization without connection key"""
        del os.environ['HANDY_CONNECTION_KEY']
        with self.assertRaises(HandyConnectionError):
            HandyController()

    def test_get_headers(self):
        """Test header generation"""
        controller = HandyController(connection_key='test_key')
        headers = controller._get_headers()
        self.assertEqual(headers['X-Connection-Key'], 'test_key')
        self.assertEqual(headers['Content-Type'], 'application/json')

    @patch('thehandy.client.requests.Session.request')
    def test_make_request_success(self, mock_request):
        """Test successful API request"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'ok'}
        mock_response.text = '{"status": "ok"}'
        mock_request.return_value = mock_response

        controller = HandyController(connection_key='test_key')
        result = controller._make_request('GET', '/status')
        self.assertEqual(result, {'status': 'ok'})

    @patch('thehandy.client.requests.Session.request')
    def test_make_request_timeout(self, mock_request):
        """Test request timeout"""
        import requests
        mock_request.side_effect = requests.Timeout()

        controller = HandyController(connection_key='test_key')
        with self.assertRaises(HandyTimeoutError):
            controller._make_request('GET', '/status')

    @patch('thehandy.client.requests.Session.request')
    def test_make_request_unauthorized(self, mock_request):
        """Test unauthorized request"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response

        controller = HandyController(connection_key='test_key')
        with self.assertRaises(HandyConnectionError):
            controller._make_request('GET', '/status')

    @patch('thehandy.client.requests.Session.request')
    def test_set_speed_valid(self, mock_request):
        """Test setting valid speed"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'speed': 50}
        mock_response.text = '{"speed": 50}'
        mock_request.return_value = mock_response

        controller = HandyController(connection_key='test_key')
        result = controller.set_speed(50)
        self.assertEqual(result['speed'], 50)

    def test_set_speed_invalid(self):
        """Test setting invalid speed"""
        controller = HandyController(connection_key='test_key')
        with self.assertRaises(ValueError):
            controller.set_speed(150)
        with self.assertRaises(ValueError):
            controller.set_speed(-10)

    @patch('thehandy.client.requests.Session.request')
    def test_set_position_valid(self, mock_request):
        """Test setting valid position"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'position': 75}
        mock_response.text = '{"position": 75}'
        mock_request.return_value = mock_response

        controller = HandyController(connection_key='test_key')
        result = controller.set_position(75)
        self.assertEqual(result['position'], 75)

    def test_set_position_invalid(self):
        """Test setting invalid position"""
        controller = HandyController(connection_key='test_key')
        with self.assertRaises(ValueError):
            controller.set_position(150)
        with self.assertRaises(ValueError):
            controller.set_position(-10)

    @patch('thehandy.client.requests.Session.request')
    def test_connect(self, mock_request):
        """Test device connection"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 'device_123', 'fw_version': '1.0'}
        mock_response.text = '{"id": "device_123"}'
        mock_request.return_value = mock_response

        controller = HandyController(connection_key='test_key')
        result = controller.connect()
        self.assertTrue(result)
        self.assertTrue(controller.is_connected())

    @patch('thehandy.client.requests.Session.close')
    def test_disconnect(self, mock_close):
        """Test device disconnection"""
        controller = HandyController(connection_key='test_key')
        controller._is_connected = True
        result = controller.disconnect()
        self.assertTrue(result)
        self.assertFalse(controller.is_connected())


if __name__ == '__main__':
    unittest.main()
