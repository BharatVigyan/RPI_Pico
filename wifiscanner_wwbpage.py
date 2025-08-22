#
# MicroPython script for Raspberry Pi Pico W
# Scans for networks, connects, and then hosts a simple web server
# to display device information.
#

import network
import time
import sys
import socket

# --- Wi-Fi Setup ---
# Initialize the WLAN interface in Station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# --- Web Page HTML ---
def web_page():
    """Generates an HTML page with device information."""
    # Using sys module to get platform and version info
    device_platform = sys.platform
    micropython_version = sys.version
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pico W Device Info</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            html {{ font-family: Helvetica, Arial, sans-serif; display: inline-block; margin: 0px auto; text-align: center; }}
            body {{ background-color: #F2F2F2; }}
            h1 {{ color: #0F3376; }}
            .info {{ font-size: 1.5rem; color: #333; }}
        </style>
    </head>
    <body>
        <h1>Raspberry Pi Pico W</h1>
        <p class="info"><strong>Board:</strong> {device_platform}</p>
        <p class="info"><strong>Firmware:</strong> {micropython_version}</p>
    </body>
    </html>
    """
    return html

# --- Function to Scan and Connect ---
def scan_and_connect():
    """
    Scans for Wi-Fi networks, prompts for credentials, connects,
    and returns the IP address on success.
    """
    print("Scanning for Wi-Fi networks...")
    networks = wlan.scan()
    
    if not networks:
        print("No networks found.")
        return None

    print("--- Available Networks ---")
    for i, net in enumerate(networks):
        ssid = net[0].decode('utf-8')
        print(f"{i + 1}: {ssid}")
    print("--------------------------")

    try:
        ssid_input = input("Enter the Wi-Fi name (SSID): ").strip()
        password_input = input(f"Enter the password for '{ssid_input}': ").strip()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return None

    if not wlan.isconnected():
        print(f"Connecting to '{ssid_input}'...")
        wlan.connect(ssid_input, password_input)
        
        max_wait = 15
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('.', end='')
            time.sleep(1)
        print()

    if wlan.status() != 3:
        print("Wi-Fi connection failed.")
        return None
    else:
        status = wlan.ifconfig()
        ip_address = status[0]
        print("--------------------------")
        print("✅ Success! Connected to Wi-Fi.")
        print(f"   IP Address: {ip_address}")
        print("--------------------------")
        return ip_address

# --- Main Execution ---
if __name__ == "__main__":
    ip_address = scan_and_connect()
    
    # Only start the web server if we have a valid IP address
    if ip_address:
        # Open a socket for the web server
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        print('Web server is listening on port 80...')

        # Main loop to listen for connections
        while True:
            try:
                cl, addr = s.accept()
                print('Client connected from', addr)
                request = cl.recv(1024)
                
                # Generate and send the HTML response
                response = web_page()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(response)
                cl.close()
                print('Client disconnected')
                
            except OSError as e:
                cl.close()
                print('Connection closed due to error')

