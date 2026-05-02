"""
Basic Joke Generator examples
"""

import sys
sys.path.insert(0, '.')

from joke_generator import JokeGenerator
from joke_generator.exceptions import JokeException


def main():
    """Basic joke generation examples"""
    print("\n=== Random Joke Generator - Basic Examples ===")
    print()

    try:
        # Create generator instance
        generator = JokeGenerator(timeout=10)

        # Example 1: Get a random joke (any type)
        print("[1] Getting a random joke (any type)...")
        print("-" * 50)
        joke = generator.get_random_joke(joke_type="any")
        formatted_joke = generator.format_joke(joke)
        print(formatted_joke)
        print()

        # Example 2: Get a programming joke
        print("[2] Getting a programming joke...")
        print("-" * 50)
        joke = generator.get_random_joke(joke_type="programming")
        formatted_joke = generator.format_joke(joke)
        print(formatted_joke)
        print()

        # Example 3: Get a general joke
        print("[3] Getting a general joke...")
        print("-" * 50)
        joke = generator.get_random_joke(joke_type="general")
        formatted_joke = generator.format_joke(joke)
        print(formatted_joke)
        print()

        # Example 4: Get from Official Joke API
        print("[4] Getting joke from Official Joke API...")
        print("-" * 50)
        joke = generator.get_official_joke()
        formatted_joke = generator.format_joke(joke)
        print(formatted_joke)
        print()

        # Close session
        generator.close()
        print("✅ Examples completed successfully!\n")

    except JokeException as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
