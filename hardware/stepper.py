# stepper.py
# All NEMA 17 / DRV8825 stepper motor functions.

from machine import Pin
import time
import config

# ═══════════════════════════════════════════════════════════
# HARDWARE SETUP
# ═══════════════════════════════════════════════════════════

step_pin = Pin(config.STEP_PIN, Pin.OUT)
dir_pin  = Pin(config.DIR_PIN,  Pin.OUT)
enable_pin = Pin(config.EN_PIN,Pin.OUT)

# Tracks absolute position in microsteps from startup position.
# The catapult must be manually pointed to your chosen 0° before power on.
_current_step_pos = 0


#ENABLE

def stepper_enable():
    """
    Enable the stepper — energises the coils so the motor holds position.
    Call before any movement.
    """
    enable_pin.value(0)   # DRV8825: LOW = enabled

def stepper_disable():
    """
    Disable the stepper — de-energises the coils.
    Call after the shot is complete to prevent the driver overheating.
    """
    enable_pin.value(1)   # DRV8825: HIGH = disabled

# ═══════════════════════════════════════════════════════════
# MOVEMENT FUNCTIONS
# ═══════════════════════════════════════════════════════════

def stepper_move(steps: int):
    """
    Move by a relative number of microsteps.
    Positive = clockwise, negative = counter-clockwise.
    """
    global _current_step_pos
    stepper_enable()
    dir_pin.value(1 if steps > 0 else 0)
    time.sleep_us(2)    # DRV8825 requires min 1µs after DIR change
    for _ in range(abs(steps)):
        step_pin.value(1)
        time.sleep_us(config.STEP_DELAY_US // 2)
        step_pin.value(0)
        time.sleep_us(config.STEP_DELAY_US // 2)
    _current_step_pos += steps

def stepper_move_to_angle(target_deg: float):
    """
    Move to an absolute angle in degrees from the startup position.
    Only moves if there is actually a difference to cover.
    """
    target_steps = round(target_deg * config.STEPS_PER_DEG)
    delta = target_steps - _current_step_pos
    if delta != 0:
        stepper_move(delta)

def stepper_reset_position():
    """
    Reset the internal position counter to zero without moving.
    Call this if you manually reposition the catapult mid-session.
    """
    global _current_step_pos
    _current_step_pos = 0
