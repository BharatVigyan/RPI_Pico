#
# MicroPython script for Raspberry Pi Pico W
# Scans for available Wi-Fi networks and prompts the user to connect
# via the serial console (e.g., Thonny Shell).
#

import network
import time
import sys

# --- Wi-Fi Setup ---
# Initialize the WLAN interface in Station mode (a device that connects to a router)
wlan = network.WLAN(network.STA_IF)
wlan.active(True) # Activate the interface

# --- Function to Scan and Connect ---
def scan_and_connect():
    """
    Scans for Wi-Fi networks, prints them, and prompts the user for credentials.
    """
    print("Scanning for Wi-Fi networks...")
    
    # wlan.scan() returns a list of tuples with network info
    # (ssid, bssid, channel, RSSI, authmode, hidden)
    networks = wlan.scan()
    
    if not networks:
        print("No networks found. Please check your location and try again.")
        return

    print("--- Available Networks ---")
    for i, net in enumerate(networks):
        # The SSID is the first item in the tuple, decode it from bytes to a string
        ssid = net[0].decode('utf-8')
        print(f"{i + 1}: {ssid}")
    print("--------------------------")

    # --- Get User Input ---
    try:
        # Prompt user to enter the desired network name (SSID)
        ssid_input = input("Enter the Wi-Fi name (SSID) you want to connect to: ").strip()
        
        # Prompt user for the password
        password_input = input(f"Enter the password for '{ssid_input}': ").strip()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return

    # --- Attempt Connection ---
    if not wlan.isconnected():
        print(f"Connecting to '{ssid_input}'...")
        wlan.connect(ssid_input, password_input)
        
        # Wait for connection with a 15-second timeout
        max_wait = 15
        while max_wait > 0:
            # wlan.status() codes:
            # 0: Link Down
            # 1: Link Join
            # 2: Link No-IP
            # 3: Link Up (Connected)
            # <0: Error
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('.', end='') # Print a dot each second as a progress indicator
            time.sleep(1)
        print() # Newline after the dots

    # --- Check Connection Status ---
    if wlan.status() != 3:
        print("Wi-Fi connection failed. Please check the SSID and password.")
    else:
        status = wlan.ifconfig()
        ip_address = status[0]
        print("--------------------------")
        print("✅ Success! Connected to Wi-Fi.")
        print(f"   IP Address: {ip_address}")
        print("--------------------------")

# --- Main Execution ---
if __name__ == "__main__":
    scan_and_connect()

