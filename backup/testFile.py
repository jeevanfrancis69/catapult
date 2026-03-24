# from machine import Pin, I2C

# # Explicitly defining the ID and the pins
# # Physical Pin 6 (GP4) and Physical Pin 7 (GP5)
# i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)

# print("Scanning...")
# devices = i2c.scan()
# if devices:
#     print("Found device(s) at:", [hex(d) for d in devices])
# else:
#     print("No I2C devices found. Check your wiring!")

# from machine import Pin
# import time

# # Setup pins
# step_pin = Pin(27, Pin.OUT)
# dir_pin = Pin(28, Pin.OUT)

# def run_test():
#     print("Moving 400 steps...")
#     dir_pin.value(1)
    
#     for i in range(3200):
#         step_pin.value(1)
#         time.sleep_us(500) # Using milliseconds for clarity
#         step_pin.value(0)
#         time.sleep_us(500)
    
#     # Force the step pin to 0 at the end
#     step_pin.value(0)
#     print("Sequence Finished.")

# # Run it once
# run_test()

# # The script ends here, so the Pico should stop pulsing.

# from machine import Pin
# import time

# # Setup Pins
# step = Pin(27, Pin.OUT)       # Physical Pin 27
# direction = Pin(28, Pin.OUT)  # Physical Pin 26
# enable = Pin(16, Pin.OUT)     # Physical Pin 21

# # IMPORTANT: Turn the motor ON (Set to 0)
# enable.value(0) 
# print("Motor Enabled")

# # Run your 200 step test
# direction.value(1)
# for i in range(3200):
#     step.value(1)
#     time.sleep_us(50)
#     step.value(0)
#     time.sleep_us(50)

# # Optional: Turn the motor OFF to save power/heat
# enable.value(1)
# print("Motor Disabled (Free spin mode)")



# from machine import Pin, PWM
# import time

# motor = Pin(21, Pin.OUT)
# motor2 = Pin(20, Pin.OUT)

# enable = Pin(16,Pin.OUT)

# enable.value(0)

# motor.value(1)
# motor2.value(0)
# time.sleep_ms(600)

# # stop
# motor.value(0)
# motor2.value(0)
# time.sleep(1)

# motor.value(0)
# motor2.value(1)

# time.sleep(1)
# motor.value(0)
# motor2.value(0)


# # Initialize Servo on GP14
# servo = PWM(Pin(14))
# servo.freq(50) # Standard 50Hz for analog servos

# def move_servo(angle):
#     # Standard range for MG90S is roughly 1000 to 9000 duty
#     # 0 degrees   = ~1638
#     # 90 degrees  = ~4915
#     # 180 degrees = ~8192
#     if 0 <= angle <= 180:
#         duty = int((angle / 180 * 6554) + 1638)
#         servo.duty_u16(duty)
#     else:
#         print("Angle must be between 0 and 180")

# # --- TEST ROUTINE ---
# try:
#     print("Testing MG90S... Press Ctrl+C to stop.")
    
#     # 1. Go to Center
#     print("Centering (90 degrees)...")
#     move_servo(90)
#     time.sleep(1)
    
#     # 2. Go to Min
#     print("Moving to 0 degrees...")
#     move_servo(0)
#     time.sleep(1)
    
#     # 3. Go to Max
#     print("Moving to 180 degrees...")
#     move_servo(180)
#     time.sleep(1)
    
#     # 4. Smooth Sweep
#     print("Starting Smooth Sweep...")
#     while True:
#         for a in range(0, 181, 5): # 0 to 180 in steps of 5
#             move_servo(a)
#             time.sleep(0.05)
#         for a in range(180, -1, -5): # 180 back to 0
#             move_servo(a)
#             time.sleep(0.05)

# except KeyboardInterrupt:
#     print("\nTest stopped by user.")
#     servo.deinit() # Turns off the PWM signal

# def set_speed(value):
#     # value: -1.0 (full reverse) → 0 (stop) → 1.0 (full forward)
#     center = 4750
#     range = 2000

#     duty = int(center + value * range)
#     servo.duty_u16(duty)

# from machine import Pin, PWM
# import time
# def add_degrees(value):
#     set_speed(-0.2)
#     time.sleep(value/50)
#     set_speed(0)

# def minus_degrees(value):
#     set_speed(0.34)
#     time.sleep(value/50)
#     set_speed(0)


# def set_speed(value):
#     center = 4750
#     span   = 2000
#     servo.duty_u16(int(center + value * span))

# test moving UP for 1 second at your speed


from machine import Pin, PWM
import time


# servo = PWM(Pin(19))
# servo.freq(50)
# servo.duty_u16(4750)  # centre/stop
# time.sleep(2)
# servo.duty_u16(6000)  # should move
# time.sleep(0.3)
# servo.duty_u16(4750)  # back to stop
from machine import Pin, PWM
import time

servo = PWM(Pin(18))
servo.freq(50)  # 50Hz for servo

def set_speed(value):
    center = 4750
    span   = 2000
    servo.duty_u16(int(center + value * span))

def add_degrees(value):
    set_speed(-0.2)
    time.sleep(value/50)
    set_speed(1)


def minus_degrees(value):
    set_speed(0.34)
    time.sleep(value/50)
    set_speed(0)



add_degrees(70)
 