# config.py
# All physical constants and pin numbers in one place.
# Change values here — no need to touch any other file.

# ═══════════════════════════════════════════════════════════
# PIN CONFIGURATION
# ═══════════════════════════════════════════════════════════

# DRV8825 stepper driver
STEP_PIN   = 27   # GP2  → STEP pin on DRV8825
DIR_PIN    = 28    # GP3  → DIR  pin on DRV8825
EN_PIN = 16

# MG996R servo
SERVO_PIN  = 19   # GP15 → orange signal wire of MG996R

# VL53L0X laser sensor (I2C)
I2C_SDA    = 2   
I2C_SCL    = 3  
I2C_ID     = 1    # Pico I2C bus 1

# ═══════════════════════════════════════════════════════════
# STEPPER CONSTANTS
# ═══════════════════════════════════════════════════════════

STEPS_PER_REV = 200     # NEMA 17 = 1.8° per step → 200 steps/rev
MICROSTEP     = 16      # match your M0/M1/M2 pin config on DRV8825
STEPS_PER_DEG = (STEPS_PER_REV * MICROSTEP) / 360.0
STEP_DELAY_US = 600     # speed of stepper — increase if skipping steps

# ═══════════════════════════════════════════════════════════
# SCAN CONSTANTS
# ═══════════════════════════════════════════════════════════

SCAN_START_DEG = 0      # where the sweep begins (your manual 0° position)
SCAN_END_DEG   = 90    # where the sweep ends
SCAN_STEP_DEG  = 5      # degrees between each reading

# ═══════════════════════════════════════════════════════════
# PROJECTILE PHYSICS CONSTANTS
# ═══════════════════════════════════════════════════════════

WHEEL_SPEED_MS = 8.0    # ball exit speed in m/s — calibrate with test shots!
GRAVITY        = 9.81   # m/s² — leave as-is

# ═══════════════════════════════════════════════════════════
# SERVO CONSTANTS
# ═══════════════════════════════════════════════════════════

SERVO_MIN_US  = 500     # pulse width in µs at 0°
SERVO_MAX_US  = 2400    # pulse width in µs at 180°
SERVO_FREQ_HZ = 50      # standard 50Hz for analogue servos
FLAP_MIN_DEG  = 15      # minimum safe flap angle
FLAP_MAX_DEG  = 45    
# ═══════════════════════════════════════════════════════════
# FLYWHEEL CONSTANTS
# ═══════════════════════════════════════════════════════════
 
FLYWHEEL_SPINUP_MS = 2000   # time to wait for flywheel to reach speed (ms) # maximum safe flap angle

# ═══════════════════════════════════════════════════════════
# SENSOR CONSTANTS
# ═══════════════════════════════════════════════════════════

VL53_TIMING_BUDGET_US = 33_000  # measurement time per reading (µs)
VL53_MAX_RANGE_MM     = 1200    # ignore readings beyond this (mm)
VL53_OUT_OF_RANGE = 8190 # indicator that target is too far
MAX_SHOTS = 5


# ═══════════════════════════════════════════════════════════
# MICRO SERVO (MG90S) — HATCH CONTROL
# ═══════════════════════════════════════════════════════════

HATCH_SERVO_PIN    = 18   # GP14 → orange signal wire of MG90S
HATCH_SERVO_FREQ_HZ = 50  # standard 50Hz for analogue servos
HATCH_MIN_US       = 500  # pulse width in µs at 0°
HATCH_MAX_US       = 2100 # pulse width in µs at 180° (MG90S specific)
HATCH_CLOSED_DEG   = 0    # angle when hatch is closed — adjust after testing
HATCH_OPEN_DEG     = 90   # angle when hatch is open — adjust after testing
HATCH_OPEN_DELAY_MS = 500 # how long hatch stays open — adjust after testing


# ═══════════════════════════════════════════════════════════
# OLED DISPLAY (SSD1306)
# ═══════════════════════════════════════════════════════════
 
DISPLAY_I2C_ID = 0    # I2C bus — note: shares bus 0 with VL53L0X
DISPLAY_SDA    = 8    # GP8  → SDA
DISPLAY_SCL    = 9    # GP9  → SCL


# ═══════════════════════════════════════════════════════════
# MOTOR FOR SPINNING WHEEL
# ═══════════════════════════════════════════════════════════
MOTOR1_PIN = 21
MOTOR2_PIN = 20