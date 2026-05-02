"""
Multiple jokes generator example
"""

import sys
sys.path.insert(0, '.')

from joke_generator import JokeGenerator
from joke_generator.exceptions import JokeException


def main():
    """Get multiple jokes examples"""
    print("\n=== Random Joke Generator - Multiple Jokes ===")
    print()

    try:
        generator = JokeGenerator()

        # Example 1: Get 5 jokes from JokeAPI
        print("[1] Getting 5 jokes from JokeAPI...")
        print("-" * 50)
        jokes = generator.get_multiple_jokes(count=5, source="jokeapi")
        
        for i, joke in enumerate(jokes, 1):
            print(f"\n📝 Joke {i}:")
            print(generator.format_joke(joke))
        print()

        # Example 2: Get 3 jokes from Official Joke API
        print("\n[2] Getting 3 jokes from Official Joke API...")
        print("-" * 50)
        jokes = generator.get_multiple_jokes(count=3, source="official")
        
        for i, joke in enumerate(jokes, 1):
            print(f"\n📝 Joke {i}:")
            print(generator.format_joke(joke))
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
