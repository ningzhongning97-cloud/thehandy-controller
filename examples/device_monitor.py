"""
Device monitor example for The Handy Controller
"""

import sys
sys.path.insert(0, '.')

from thehandy import HandyController
from thehandy.exceptions import HandyException
import time
from datetime import datetime


def print_status(controller):
    """Print current device status"""
    try:
        status = controller.get_status()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Status: {status}")
        return status
    except Exception as e:
        print(f"Error getting status: {e}")
        return None


def main():
    """Device monitor example"""
    try:
        controller = HandyController()

        print("\n=== The Handy Controller - Device Monitor Example ===")
        print()

        # Connect to device
        print("[*] Connecting to device...")
        controller.connect()
        print("✓ Connected successfully!\n")

        # Get initial device info
        print("[*] Device information:")
        device_info = controller.get_device_info()
        for key, value in device_info.items():
            print(f"  {key}: {value}")
        print()

        # Monitor device for 30 seconds
        print("[*] Monitoring device status (30 seconds)...")
        print("Press Ctrl+C to stop\n")

        monitor_duration = 30
        interval = 5  # Check every 5 seconds
        elapsed = 0

        while elapsed < monitor_duration:
            print_status(controller)
            time.sleep(interval)
            elapsed += interval

        print()
        print("[*] Setting various speeds to demonstrate monitoring...\n")

        # Set speeds and monitor
        speeds = [25, 50, 75, 100, 50, 25, 0]
        for speed in speeds:
            print(f"Setting speed to {speed}...")
            controller.set_speed(speed)
            print_status(controller)
            time.sleep(2)

        print()
        print("[*] Disconnecting...")
        controller.disconnect()
        print("✓ Disconnected successfully!\n")

        print("=== Monitoring completed ===")

    except KeyboardInterrupt:
        print("\n\n[!] Monitoring interrupted by user")
        try:
            controller.disconnect()
        except:
            pass
        sys.exit(0)
    except HandyException as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
