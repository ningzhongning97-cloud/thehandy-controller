"""
Joke types example - demonstrating different joke categories
"""

import sys
sys.path.insert(0, '.')

from joke_generator import JokeGenerator
from joke_generator.exceptions import JokeException


def main():
    """Get jokes by specific types"""
    print("\n=== Random Joke Generator - Joke Types ===")
    print()

    try:
        generator = JokeGenerator()

        # Available joke types
        joke_types = ["general", "programming", "knock-knock", "any"]

        for joke_type in joke_types:
            print(f"[*] Getting a {joke_type} joke...")
            print("-" * 50)
            try:
                joke = generator.get_joke_by_type(joke_type)
                formatted_joke = generator.format_joke(joke)
                print(formatted_joke)
            except JokeException as e:
                print(f"⚠️  Could not fetch {joke_type} joke: {e}")
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
