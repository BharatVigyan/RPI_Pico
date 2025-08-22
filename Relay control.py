#
# MicroPython script to control a relay via USB serial commands.
# Listens for "on" and "off" commands from a serial monitor (e.g., Thonny Shell).
# The onboard LED will mirror the state of the relay.
#

import machine
import sys
import time

# --- Pin Configuration ---
# Set the GPIO pin connected to the relay's IN pin. We are using GP15.
RELAY_PIN = 15
relay = machine.Pin(RELAY_PIN, machine.Pin.OUT)

# Initialize the onboard LED for status indication.
led = machine.Pin("LED", machine.Pin.OUT)


# --- Initial State ---
# We need to set the initial state of the relay to OFF.
# NOTE: Most common relay modules are "active-low". This means you send a
# LOW signal (0V) to turn them ON and a HIGH signal (3.3V) to turn them OFF.
# If your relay works the other way (active-high), swap .high() and .low() below.
print("Setting initial state: Relay OFF")
relay.high()  # Set pin HIGH to keep the active-low relay OFF.
led.off()     # Turn the onboard LED off.


# --- Main Loop ---
print("--------------------------")
print("Relay Control is Ready!")
print("Enter 'on' or 'off' and press Enter.")
print("--------------------------")

while True:
    # Read a line from the standard input (the USB serial connection)
    command = sys.stdin.readline().strip()

    # The .strip() function removes any hidden newline or space characters.
    # We also convert the command to lowercase to make it case-insensitive.
    if command.lower() == "on":
        print("Received command: ON")
        relay.low()  # Turn the active-low relay ON
        led.on()     # Turn the status LED ON

    elif command.lower() == "off":
        print("Received command: OFF")
        relay.high() # Turn the active-low relay OFF
        led.off()    # Turn the status LED OFF
        
    # We add a small delay to prevent the loop from running too fast.
    time.sleep(0.1)

