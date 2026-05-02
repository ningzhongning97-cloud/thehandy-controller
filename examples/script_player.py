"""
Script player example for The Handy Controller
"""

import sys
sys.path.insert(0, '.')

from thehandy import HandyController
from thehandy.exceptions import HandyException
import time


def main():
    """Script player example"""
    try:
        controller = HandyController()

        print("\n=== The Handy Controller - Script Player Example ===")
        print()

        # Connect to device
        print("[1] Connecting to device...")
        controller.connect()
        print("✓ Connected successfully!\n")

        # Get available scripts
        print("[2] Fetching available scripts...")
        try:
            scripts = controller.get_scripts()
            print(f"Available scripts: {scripts}")
            print()
        except Exception as e:
            print(f"Note: Could not fetch scripts: {e}")
            print("Continuing with demo...\n")

        # Play a script (example with script ID)
        script_id = "sample_script_1"  # Replace with actual script ID
        print(f"[3] Playing script '{script_id}'...")
        try:
            result = controller.play_script(script_id)
            print(f"✓ Script started: {result}")
            print()

            # Let script play for a while
            print("[4] Script is playing for 5 seconds...")
            time.sleep(5)

            # Pause script
            print("\n[5] Pausing script...")
            controller.pause_script()
            print("✓ Script paused!")
            print()

            # Wait a bit
            time.sleep(2)

            # Resume script
            print("[6] Resuming script...")
            controller.resume_script()
            print("✓ Script resumed!")
            print()

            # Let it play a bit more
            time.sleep(3)

            # Stop device
            print("\n[7] Stopping device...")
            controller.stop()
            print("✓ Device stopped!\n")

        except HandyException as e:
            print(f"Script playback error: {e}")
            print("This is expected if the script doesn't exist.")
            print()

        # Disconnect
        print("[8] Disconnecting...")
        controller.disconnect()
        print("✓ Disconnected successfully!\n")

        print("=== Example completed ===")

    except HandyException as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
