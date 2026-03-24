# micro_servo.py
# MG90S micro servo functions for hatch control.

from machine import Pin, PWM
import time
import config

# ═══════════════════════════════════════════════════════════
# HARDWARE SETUP
# ═══════════════════════════════════════════════════════════

_hatch_pwm = PWM(Pin(config.HATCH_SERVO_PIN))
_hatch_pwm.freq(config.HATCH_SERVO_FREQ_HZ)

# ═══════════════════════════════════════════════════════════
# HATCH FUNCTIONS
# ═══════════════════════════════════════════════════════════

def _angle_to_duty(angle_deg: float) -> int:
    """
    Convert angle (0-180°) to 16-bit PWM duty value for the Pico.
    Uses MG90S specific min/max pulse widths from config.
    """
    pulse_us  = config.HATCH_MIN_US + (angle_deg / 180.0) * (config.HATCH_MAX_US - config.HATCH_MIN_US)
    period_us = 1_000_000 / config.HATCH_SERVO_FREQ_HZ
    return int((pulse_us / period_us) * 65535)

def hatch_open():
    """Open the hatch to let the ball drop into the flywheel."""
    _hatch_pwm.duty_u16(_angle_to_duty(config.HATCH_OPEN_DEG))
    time.sleep_ms(400)   # wait for servo to reach position

def hatch_close():
    """Close the hatch to hold the ball back."""
    _hatch_pwm.duty_u16(_angle_to_duty(config.HATCH_CLOSED_DEG))
    time.sleep_ms(400)   # wait for servo to reach position
