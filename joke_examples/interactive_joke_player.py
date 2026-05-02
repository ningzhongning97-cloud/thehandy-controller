"""
Interactive Joke Player - A fun interactive joke application
"""

import sys
sys.path.insert(0, '.')

from joke_generator import JokeGenerator
from joke_generator.exceptions import JokeException
import time


def print_menu():
    """Print the menu"""
    print("\n" + "=" * 50)
    print("   Random Joke Generator - Interactive Player")
    print("=" * 50)
    print("[1] Get a random joke (any type)")
    print("[2] Get a programming joke")
    print("[3] Get a general joke")
    print("[4] Get a knock-knock joke")
    print("[5] Get multiple jokes")
    print("[6] Get from Official Joke API")
    print("[0] Exit")
    print("=" * 50)


def get_random_joke(generator):
    """Get and display a random joke"""
    try:
        print("\n🔄 Fetching joke...")
        joke = generator.get_random_joke(joke_type="any")
        joke_text = generator.format_joke(joke)
        
        print("\n" + "=" * 50)
        print("📝 Here's your joke:")
        print("=" * 50)
        print(joke_text)
        print("=" * 50)
    except JokeException as e:
        print(f"❌ Error: {e}")


def get_typed_joke(generator, joke_type):
    """Get a joke by type"""
    try:
        print(f"\n🔄 Fetching {joke_type} joke...")
        joke = generator.get_joke_by_type(joke_type)
        joke_text = generator.format_joke(joke)
        
        print("\n" + "=" * 50)
        print(f"📝 Here's your {joke_type} joke:")
        print("=" * 50)
        print(joke_text)
        print("=" * 50)
    except JokeException as e:
        print(f"❌ Error: {e}")


def get_multiple_jokes(generator):
    """Get multiple jokes"""
    try:
        count = input("\nHow many jokes do you want? (1-10): ").strip()
        count = int(count)
        if count < 1 or count > 10:
            print("❌ Please enter a number between 1 and 10")
            return
        
        print(f"\n🔄 Fetching {count} jokes...")
        jokes = generator.get_multiple_jokes(count=count, source="jokeapi")
        
        print("\n" + "=" * 50)
        print(f"📝 Here are your {count} jokes:")
        print("=" * 50)
        
        for i, joke in enumerate(jokes, 1):
            print(f"\n[Joke {i}]")
            print(generator.format_joke(joke))
            print("-" * 50)
        
        print()
    except ValueError:
        print("❌ Please enter a valid number")
    except JokeException as e:
        print(f"❌ Error: {e}")


def get_official_joke(generator):
    """Get a joke from Official Joke API"""
    try:
        print("\n🔄 Fetching joke from Official Joke API...")
        joke = generator.get_official_joke()
        joke_text = generator.format_joke(joke)
        
        print("\n" + "=" * 50)
        print("📝 Here's your joke from Official Joke API:")
        print("=" * 50)
        print(joke_text)
        print("=" * 50)
    except JokeException as e:
        print(f"❌ Error: {e}")


def main():
    """Main interactive loop"""
    print("\n✅ Joke Generator initialized!\n")
    
    try:
        generator = JokeGenerator()
        
        while True:
            print_menu()
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == "1":
                get_random_joke(generator)
            elif choice == "2":
                get_typed_joke(generator, "programming")
            elif choice == "3":
                get_typed_joke(generator, "general")
            elif choice == "4":
                get_typed_joke(generator, "knock-knock")
            elif choice == "5":
                get_multiple_jokes(generator)
            elif choice == "6":
                get_official_joke(generator)
            elif choice == "0":
                print("\n👋 Thanks for using Joke Generator!\n")
                break
            else:
                print("❌ Invalid choice. Please try again.")
            
            time.sleep(0.5)
        
        generator.close()

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        try:
            generator.close()
        except:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
