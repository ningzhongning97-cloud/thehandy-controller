"""
Basic control example for The Handy Controller
"""

import sys
sys.path.insert(0, '.')

from thehandy import HandyController
from thehandy.exceptions import HandyException
import time


def main():
    """Basic control example"""
    try:
        # Initialize the controller with connection key
        # You can pass the key directly or use environment variable HANDY_CONNECTION_KEY
        controller = HandyController()

        print("\n=== The Handy Controller - Basic Control Example ===")
        print()

        # Connect to device
        print("[1] Connecting to device...")
        controller.connect()
        print("✓ Connected successfully!\n")

        # Get device info
        print("[2] Getting device information...")
        device_info = controller.get_device_info()
        print(f"Device Info: {device_info}\n")

        # Get device status
        print("[3] Getting device status...")
        status = controller.get_status()
        print(f"Status: {status}\n")

        # Set speed
        print("[4] Setting speed to 50...")
        controller.set_speed(50)
        print("✓ Speed set successfully!\n")
        time.sleep(1)

        # Set position
        print("[5] Setting position to 75...")
        controller.set_position(75)
        print("✓ Position set successfully!\n")
        time.sleep(1)

        # Get available scripts
        print("[6] Getting available scripts...")
        try:
            scripts = controller.get_scripts()
            print(f"Available scripts: {scripts}\n")
        except Exception as e:
            print(f"Could not fetch scripts: {e}\n")

        # Stop device
        print("[7] Stopping device...")
        controller.stop()
        print("✓ Device stopped!\n")

        # Disconnect
        print("[8] Disconnecting...")
        controller.disconnect()
        print("✓ Disconnected successfully!\n")

        print("=== Example completed successfully ===")

    except HandyException as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
