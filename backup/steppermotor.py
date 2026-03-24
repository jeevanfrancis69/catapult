from machine import Pin
import time

# DRV8825 pins
STEP = Pin(2, Pin.OUT)
DIR  = Pin(1, Pin.OUT)



DIR.value(1)   # 1 = one direction, 0 = other

def step(n, delay_ms=2):
    for _ in range(n):
        STEP.value(1)
        time.sleep_ms(delay_ms)
        STEP.value(0)
        time.sleep_ms(delay_ms)

# Test: 200 steps = 1 full revolution (assuming 1/1 full step mode)
step(200)
time.sleep(1)

DIR.value(0)   # reverse
step(200)