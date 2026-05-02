# Random Joke Generator 🎭

A Python library for generating random jokes using external APIs. Supports multiple joke sources and categories.

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 🎉 Features

- ✅ Multiple joke sources (JokeAPI, Official Joke API)
- ✅ Various joke categories (general, programming, knock-knock)
- ✅ Fetch single or multiple jokes
- ✅ Easy-to-use API
- ✅ Comprehensive error handling
- ✅ Logging support
- ✅ Interactive joke player
- ✅ Full unit test coverage

## 📋 Requirements

- Python 3.7+
- pip

## 📦 Installation

### From source

```bash
# If in the thehandy-controller project
pip install requests
```

### Dependencies

```bash
pip install requests
```

## 🚀 Quick Start

### Basic Usage

```python
from joke_generator import JokeGenerator

# Create generator instance
generator = JokeGenerator()

# Get a random joke
joke = generator.get_random_joke(joke_type="any")
formatted_joke = generator.format_joke(joke)
print(formatted_joke)

# Get a programming joke
joke = generator.get_random_joke(joke_type="programming")
print(generator.format_joke(joke))

# Close session
generator.close()
```

## 📚 API Reference

### JokeGenerator Class

#### Initialization

```python
generator = JokeGenerator(timeout=10)
```

**Parameters:**
- `timeout` (int): Request timeout in seconds (default: 10)

#### Methods

##### `get_random_joke(joke_type="any")`

Get a random joke from JokeAPI.

```python
joke = generator.get_random_joke(joke_type="programming")
```

**Parameters:**
- `joke_type` (str): Type of joke - `'general'`, `'programming'`, `'knock-knock'`, or `'any'`

**Returns:** Dictionary with joke data

**Raises:** `JokeException` if request fails

---

##### `get_official_joke()`

Get a random joke from Official Joke API.

```python
joke = generator.get_official_joke()
```

**Returns:** Dictionary with joke data

**Raises:** `JokeException` if request fails

---

##### `get_multiple_jokes(count=5, source="jokeapi")`

Get multiple random jokes.

```python
jokes = generator.get_multiple_jokes(count=5, source="jokeapi")
```

**Parameters:**
- `count` (int): Number of jokes to fetch (default: 5, max: 10)
- `source` (str): API source - `'jokeapi'` or `'official'` (default: `'jokeapi'`)

**Returns:** List of joke dictionaries

**Raises:** `JokeException` if request fails

---

##### `get_joke_by_type(joke_type)`

Get a joke by specific type.

```python
joke = generator.get_joke_by_type("programming")
```

**Parameters:**
- `joke_type` (str): Type of joke - `'general'` or `'programming'`

**Returns:** Dictionary with joke data

**Raises:** `JokeAPIError` if invalid type is provided

---

##### `format_joke(joke)`

Format joke data into readable string.

```python
joke = generator.get_random_joke()
formatted = generator.format_joke(joke)
print(formatted)
```

**Parameters:**
- `joke` (dict): Joke dictionary

**Returns:** Formatted joke string

---

##### `close()`

Close the HTTP session.

```python
generator.close()
```

## 🎯 Examples

### Example 1: Basic Jokes

```python
from joke_generator import JokeGenerator

generator = JokeGenerator()

# Get and display a random joke
joke = generator.get_random_joke(joke_type="any")
print(generator.format_joke(joke))

# Get a programming joke
joke = generator.get_random_joke(joke_type="programming")
print(generator.format_joke(joke))

generator.close()
```

Run: `python joke_examples/basic_jokes.py`

### Example 2: Multiple Jokes

```python
from joke_generator import JokeGenerator

generator = JokeGenerator()

# Get 5 jokes
jokes = generator.get_multiple_jokes(count=5)
for i, joke in enumerate(jokes, 1):
    print(f"[Joke {i}]")
    print(generator.format_joke(joke))
    print()

generator.close()
```

Run: `python joke_examples/multiple_jokes.py`

### Example 3: Joke Types

```python
from joke_generator import JokeGenerator

generator = JokeGenerator()

joke_types = ["general", "programming", "knock-knock"]
for joke_type in joke_types:
    joke = generator.get_joke_by_type(joke_type)
    print(f"[{joke_type}]")
    print(generator.format_joke(joke))
    print()

generator.close()
```

Run: `python joke_examples/joke_types.py`

### Example 4: Interactive Joke Player

```bash
python joke_examples/interactive_joke_player.py
```

An interactive application to play jokes:
- Get random jokes
- Get jokes by type
- Get multiple jokes
- Switch between different APIs

## 🧪 Testing

Run unit tests:

```bash
python -m pytest joke_tests/
```

Or with unittest:

```bash
python -m unittest discover joke_tests/
```

## 🛡️ Error Handling

The library provides custom exceptions for different error scenarios:

```python
from joke_generator import (
    JokeException,      # Base exception
    JokeAPIError,       # API request errors
    JokeTimeoutError,   # Request timeout
    JokeNetworkError,   # Network connection errors
)

try:
    generator = JokeGenerator()
    joke = generator.get_random_joke()
except JokeTimeoutError:
    print("Request timed out")
except JokeNetworkError:
    print("Network connection error")
except JokeAPIError as e:
    print(f"API error: {e}")
except JokeException as e:
    print(f"Other error: {e}")
finally:
    generator.close()
```

## 📁 Project Structure

```
joke_generator/
├── __init__.py          # Package initialization
├── generator.py         # Main generator class
└── exceptions.py        # Custom exceptions

joke_examples/
├── basic_jokes.py       # Basic usage examples
├── multiple_jokes.py    # Multiple jokes examples
├── joke_types.py        # Different joke types
└── interactive_joke_player.py  # Interactive application

joke_tests/
├── __init__.py
└── test_generator.py    # Unit tests
```

## 🔗 External APIs

### JokeAPI (v2)
- **Base URL:** `https://v2.jokeapi.dev`
- **Endpoints:** `/joke/{type}` (general, programming, knock-knock, any)
- **Features:** Two-part jokes, single jokes, filtering

### Official Joke API
- **Base URL:** `https://official-joke-api.appspot.com`
- **Endpoints:** `/random_joke`
- **Features:** Random jokes, simple format

## 🔒 Rate Limiting

Both APIs have rate limiting:
- JokeAPI: 120 requests per minute
- Official Joke API: Generally generous rate limits

## 📝 Logging

The generator uses Python's built-in logging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('joke_generator')
```

## 🐛 Troubleshooting

### Timeout Error

```python
# Increase timeout
generator = JokeGenerator(timeout=20)
```

### Network Error

- Check your internet connection
- Try again after a moment
- Check if the API is up at https://jokeapi.dev

### No Jokes Available

- Try a different joke type
- Try the official joke API
- Check the API rate limiting

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 🔗 Links

- [JokeAPI Documentation](https://jokeapi.dev)
- [Official Joke API](https://official-joke-api.appspot.com)
- [GitHub Repository](https://github.com/ningzhongning97-cloud/thehandy-controller)

---

**Last Updated:** 2026-05-02
