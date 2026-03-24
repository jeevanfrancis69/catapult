from machine import I2C, Pin
import time
from vl53l0x import VL53L0X

# 1. Setup the Hardware
# Using I2C1, SDA=GP6, SCL=GP7
i2c = I2C(1, sda=Pin(6), scl=Pin(7))

# 2. Initialize the Sensor
try:
    tof = VL53L0X(i2c)
    print("Distance Sensor: Connected")
except Exception as e:
    print(f"Distance Sensor: Failed to connect! Error: {e}")
    tof = None

def get_mm():
    """Returns distance in millimeters. Returns -1 if sensor is disconnected."""
    if tof is None:
        return -1
    try:
        # Using .range as identified in your library file
        return tof.range
    except:
        return -1

# --- SELF-TEST SECTION ---
# This part only runs if you play THIS file directly. 
# It won't run when you import it into main.py later.
if __name__ == "__main__":
    print("Starting Self-Test...")
    while True:
        reading = get_mm()
        if reading == -1:
            print("Error: Sensor not responding.")
        else:
            print(f"Current Distance: {reading} mm")
        time.sleep(0.5)