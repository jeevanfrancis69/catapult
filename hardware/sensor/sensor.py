# sensor.py
# All VL53L0X laser distance sensor functions.

from machine import I2C, Pin
import time
import vl53l0x
import config

# ═══════════════════════════════════════════════════════════
# HARDWARE SETUP
# ═══════════════════════════════════════════════════════════

def init_sensor():
    """
    Initialise the VL53L0X sensor over I2C.
    Raises OSError if sensor is not found — check your SDA/SCL wiring.
    Call this once at the start of main.py.
    """
    try:
        i2c = I2C(config.I2C_ID,
                  sda=Pin(config.I2C_SDA),
                  scl=Pin(config.I2C_SCL),
                  freq=400_000)
        sensor = vl53l0x.VL53L0X(i2c)
        sensor.measurement_timing_budget = config.VL53_TIMING_BUDGET_US
        print("Sensor initialised.")
        return sensor
    except OSError as e:
        raise OSError(f"Sensor init failed — check I2C wiring (SDA=GP{config.I2C_SDA}, SCL=GP{config.I2C_SCL}): {e}")

# ═══════════════════════════════════════════════════════════
# READING FUNCTIONS
# ═══════════════════════════════════════════════════════════

def read_distance_mm(sensor) -> float:
    """
    Single distance reading in mm.
    Returns float('inf') if out of range or invalid.
    """
    reading = sensor.read_range_single_millimeters()
    if reading is None or reading >= config.VL53_MAX_RANGE_MM:
        return float('inf')
    return float(reading)

def read_distance_averaged_mm(sensor, samples: int = 3) -> float:
    """
    Average multiple readings to reduce noise.
    Returns float('inf') if no valid readings were obtained.
    """
    valid = []
    for i in range(samples):
        d = read_distance_mm(sensor)
        if d != float('inf'):
            valid.append(d)
        time.sleep_ms(10)
    if not valid:
        return float('inf')
    return sum(valid) / len(valid)
