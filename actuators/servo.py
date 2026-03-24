# servo.py
# All MG996R servo functions for up/down flap control.

from machine import Pin, PWM
import time
import config

# ═══════════════════════════════════════════════════════════
# HARDWARE SETUP
# ═══════════════════════════════════════════════════════════

_servo_pwm = PWM(Pin(config.SERVO_PIN))
_servo_pwm.freq(config.SERVO_FREQ_HZ)

# ═══════════════════════════════════════════════════════════
# SERVO FUNCTIONS
# ═══════════════════════════════════════════════════════════

def _angle_to_duty(angle_deg: float) -> int:
    """
    Convert angle (0-180°) to a 16-bit PWM duty value for the Pico.
    Pico PWM duty range: 0-65535 representing 0-100% of the 20ms period.
    Not called directly — used internally by servo_set_angle.
    """
    pulse_us  = config.SERVO_MIN_US + (angle_deg / 180.0) * (config.SERVO_MAX_US - config.SERVO_MIN_US)
    period_us = 1_000_000 / config.SERVO_FREQ_HZ   # = 20,000 µs at 50Hz
    return int((pulse_us / period_us) * 65535)

def servo_set_angle(angle_deg: float):
    """
    Set the flap to the given angle in degrees.
    Automatically clamps to FLAP_MIN_DEG and FLAP_MAX_DEG
    so the servo can never be driven into a physical hard stop.
    """
    angle_deg = max(config.FLAP_MIN_DEG, min(config.FLAP_MAX_DEG, angle_deg))
    _servo_pwm.duty_u16(_angle_to_duty(angle_deg))
    time.sleep_ms(400)  # wait for servo to physically reach position

def servo_neutral():
    """
    Move flap to neutral mid-range position.
    Called at startup and after each shot.
    """
    servo_set_angle((config.FLAP_MIN_DEG + config.FLAP_MAX_DEG) / 2)
