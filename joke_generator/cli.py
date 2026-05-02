"""
Command-line interface for Joke Generator
"""

import argparse
import sys
from .generator import JokeGenerator
from .exceptions import JokeException


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Random Joke Generator - Get jokes from the command line",
        prog="joke-generator",
    )
    
    parser.add_argument(
        "--type",
        "-t",
        choices=["any", "general", "programming", "knock-knock"],
        default="any",
        help="Type of joke (default: any)",
    )
    
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=1,
        help="Number of jokes (default: 1, max: 10)",
    )
    
    parser.add_argument(
        "--source",
        "-s",
        choices=["jokeapi", "official"],
        default="jokeapi",
        help="Joke source API (default: jokeapi)",
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)",
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    
    args = parser.parse_args()
    
    try:
        generator = JokeGenerator(timeout=args.timeout)
        
        if args.count == 1:
            if args.source == "official":
                joke = generator.get_official_joke()
            else:
                joke = generator.get_joke_by_type(args.type)
            
            formatted_joke = generator.format_joke(joke)
            print(formatted_joke)
        else:
            jokes = generator.get_multiple_jokes(count=args.count, source=args.source)
            for i, joke in enumerate(jokes, 1):
                print(f"\n[Joke {i}]")
                print(generator.format_joke(joke))
        
        generator.close()
    
    except JokeException as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
