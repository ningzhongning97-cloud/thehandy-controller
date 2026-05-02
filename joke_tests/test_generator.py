"""
Unit tests for Joke Generator
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from joke_generator import JokeGenerator
from joke_generator.exceptions import (
    JokeAPIError,
    JokeTimeoutError,
    JokeNetworkError,
)


class TestJokeGenerator(unittest.TestCase):
    """Test cases for JokeGenerator"""

    def setUp(self):
        """Set up test fixtures"""
        self.generator = JokeGenerator(timeout=5)

    def tearDown(self):
        """Clean up after tests"""
        try:
            self.generator.close()
        except:
            pass

    def test_generator_initialization(self):
        """Test generator initialization"""
        self.assertEqual(self.generator.timeout, 5)
        self.assertIsNotNone(self.generator.session)

    @patch('joke_generator.generator.requests.Session.get')
    def test_get_random_joke_success(self, mock_get):
        """Test successful random joke fetch"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "type": "twopart",
            "setup": "Why did the programmer quit his job?",
            "delivery": "Because he didn't get arrays.",
            "category": "Programming",
        }
        mock_get.return_value = mock_response

        joke = self.generator.get_random_joke(joke_type="programming")
        self.assertIn("setup", joke)
        self.assertIn("delivery", joke)

    @patch('joke_generator.generator.requests.Session.get')
    def test_get_random_joke_timeout(self, mock_get):
        """Test timeout error"""
        import requests
        mock_get.side_effect = requests.Timeout()

        with self.assertRaises(JokeTimeoutError):
            self.generator.get_random_joke()

    @patch('joke_generator.generator.requests.Session.get')
    def test_get_random_joke_connection_error(self, mock_get):
        """Test network connection error"""
        import requests
        mock_get.side_effect = requests.ConnectionError()

        with self.assertRaises(JokeNetworkError):
            self.generator.get_random_joke()

    @patch('joke_generator.generator.requests.Session.get')
    def test_get_official_joke_success(self, mock_get):
        """Test successful official joke fetch"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "type": "general",
            "setup": "What do you call a bear with no teeth?",
            "punchline": "A gummy bear!",
        }
        mock_get.return_value = mock_response

        joke = self.generator.get_official_joke()
        self.assertIn("setup", joke)
        self.assertIn("punchline", joke)

    def test_format_joke_twopart(self):
        """Test formatting two-part joke"""
        joke = {
            "setup": "Why did the programmer quit?",
            "delivery": "He didn't like his job."
        }
        formatted = self.generator.format_joke(joke)
        self.assertIn("Why did the programmer quit?", formatted)
        self.assertIn("He didn't like his job.", formatted)

    def test_format_joke_punchline(self):
        """Test formatting joke with punchline"""
        joke = {
            "setup": "What do you call a bear with no teeth?",
            "punchline": "A gummy bear!"
        }
        formatted = self.generator.format_joke(joke)
        self.assertIn("What do you call a bear with no teeth?", formatted)
        self.assertIn("A gummy bear!", formatted)

    def test_format_joke_single(self):
        """Test formatting single joke"""
        joke = {
            "joke": "Why don't scientists trust atoms? Because they make up everything!"
        }
        formatted = self.generator.format_joke(joke)
        self.assertIn("Why don't scientists trust atoms?", formatted)

    def test_get_joke_by_type_valid(self):
        """Test get joke by valid type"""
        valid_types = ["general", "programming", "knock-knock", "any"]
        for joke_type in valid_types:
            with patch.object(self.generator, 'get_random_joke', return_value={"setup": "test", "delivery": "test"}):
                result = self.generator.get_joke_by_type(joke_type)
                self.assertIsNotNone(result)

    def test_get_joke_by_type_invalid(self):
        """Test get joke by invalid type"""
        with self.assertRaises(JokeAPIError):
            self.generator.get_joke_by_type("invalid_type")

    @patch.object(JokeGenerator, 'get_random_joke')
    def test_get_multiple_jokes(self, mock_get_joke):
        """Test getting multiple jokes"""
        mock_get_joke.return_value = {"setup": "test", "delivery": "test"}
        
        jokes = self.generator.get_multiple_jokes(count=3)
        self.assertEqual(len(jokes), 3)
        self.assertEqual(mock_get_joke.call_count, 3)

    def test_close_session(self):
        """Test closing session"""
        gen = JokeGenerator()
        gen.close()
        # Should not raise an error
        self.assertIsNotNone(gen.session)


if __name__ == '__main__':
    unittest.main()
