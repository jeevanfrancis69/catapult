# main.py
# Catapult auto-aim algorithm.
# Sequence: init → scan → acquire target → aim → fire until destroyed
#
# BEFORE RUNNING:
#   1. Manually point the catapult to your chosen 0° position
#   2. VL53L0X wired to GP20 (SDA) and GP21 (SCL)
#   3. SSD1306 wired to GP8 (SDA) and GP9 (SCL)
#   4. Calibrate WHEEL_SPEED_MS in config.py with test shots

import time
import math
import config
from sensor      import init_sensor, read_distance_averaged_mm
from stepper     import stepper_move_to_angle, stepper_disable
from servo       import servo_set_angle, servo_neutral
from micro_servo import hatch_open, hatch_close
from display     import (init_display, show_scanning, show_target_found,
                         show_firing, show_target_destroyed, show_no_target)

# ═══════════════════════════════════════════════════════════
# SCAN
# ═══════════════════════════════════════════════════════════

def scan_targets(sensor) -> list:
    """
    Sweep the stepper across the scan arc.
    Returns a list of (angle_deg, distance_mm) for all valid readings.
    Returns empty list if nothing detected.
    """
    readings = []
    angle = config.SCAN_START_DEG

    print(f"Scanning {config.SCAN_START_DEG}° to "
          f"{config.SCAN_END_DEG}° in {config.SCAN_STEP_DEG}° steps...")

    while angle <= config.SCAN_END_DEG:
        stepper_move_to_angle(angle)
        time.sleep_ms(50)
        dist = read_distance_averaged_mm(sensor, 3)

        if dist != -1:
            readings.append((angle, dist))
            print(f"  {angle:5.1f}°  →  {dist:6.1f} mm")
        else:
            print(f"  {angle:5.1f}°  →  no return")

        angle += config.SCAN_STEP_DEG

    return readings

def find_nearest(readings: list):
    """Return (angle, distance_mm) of the closest detected object."""
    return min(readings, key=lambda r: r[1])

# ═══════════════════════════════════════════════════════════
# PHYSICS
# ═══════════════════════════════════════════════════════════

def calculate_launch_angle(distance_m: float) -> float:
    """
    Solve for slab angle θ using flat-ground projectile motion.
    Raises ValueError if target is out of range.
    """
    ratio = (distance_m * config.GRAVITY) / (config.WHEEL_SPEED_MS ** 2)
    if ratio > 1.0:
        max_range = (config.WHEEL_SPEED_MS ** 2) / config.GRAVITY
        raise ValueError(
            f"Target {distance_m:.2f}m out of range. "
            f"Max = {max_range:.2f}m at {config.WHEEL_SPEED_MS}m/s."
        )
    theta_rad = 0.5 * math.asin(ratio)
    return math.degrees(theta_rad)

# ═══════════════════════════════════════════════════════════
# TARGET DESTROYED CHECK
# ═══════════════════════════════════════════════════════════

def target_is_gone(sensor) -> bool:
    """
    Re-scan after firing — stepper stays at target angle throughout.
    Returns True if the target is no longer detected.
    The VL53L0X returns >= 8190 when nothing is in range.
    """
    time.sleep_ms(200)
    dist = read_distance_averaged_mm(sensor, 3)
    print(f"Post-shot check: {dist:.0f} mm")
    return dist == -1 or dist >= config.VL53_OUT_OF_RANGE

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main():
    print("=== Catapult auto-aim starting ===")
    print("Make sure catapult is manually pointed to 0° before continuing.")

    # ── Initialise display ──────────────────────────────────
    try:
        oled = init_display()
    except OSError as e:
        print(f"ERROR: {e}")
        return

    # ── Initialise sensor ───────────────────────────────────
    try:
        sensor = init_sensor()
    except OSError as e:
        print(f"ERROR: {e}")
        return

    # ── Set slab to neutral, ensure hatch is closed ─────────
    servo_neutral()
    hatch_close()

    # ── Scan ────────────────────────────────────────────────
    show_scanning(oled)
    readings = scan_targets(sensor)

    if not readings:
        print("No targets detected. Standby.")
        show_no_target(oled)
        return

    # ── Find nearest target ─────────────────────────────────
    target_angle, target_dist_mm = find_nearest(readings)
    target_dist_m = target_dist_mm / 1000.0
    print(f"\nTarget acquired: {target_dist_mm:.0f}mm at {target_angle:.1f}°")
    show_target_found(oled, target_dist_mm)

    # ── Calculate slab angle ────────────────────────────────
    try:
        theta = calculate_launch_angle(target_dist_m)
    except ValueError as e:
        print(f"ERROR: {e}")
        return
    print(f"Slab angle: {theta:.2f}°")

    # ── Aim ─────────────────────────────────────────────────
    print(f"Rotating to {target_angle:.1f}°...")
    stepper_move_to_angle(target_angle)

    print(f"Setting slab to {theta:.2f}°...")
    servo_set_angle(theta)

    # ── Fire loop — keep firing until target is gone ────────
    shot_count = 0

    while True:
        shot_count += 1
        print(f"Shot {shot_count} of max {config.MAX_SHOTS}")
        show_firing(oled)

        # spin up flywheel
        print(f"Spinning up flywheel ({config.FLYWHEEL_SPINUP_MS}ms)...")
        # flywheel start code goes here
        time.sleep_ms(config.FLYWHEEL_SPINUP_MS)

        # fire
        hatch_open()
        time.sleep_ms(config.HATCH_OPEN_DELAY_MS)
        hatch_close()

        # pause before checking
        time.sleep_ms(500)

        # check if target is gone
        if target_is_gone(sensor):
            print("Target destroyed!")
            show_target_destroyed(oled)
            break

        # safety limit — stop if max shots reached
        if shot_count >= config.MAX_SHOTS:
            print(f"Max shots ({config.MAX_SHOTS}) reached. Stopping.")
            break

        print("Target still detected. Firing again...")

    # ── Reset ───────────────────────────────────────────────
    servo_neutral()
    stepper_disable()
    print("=== Sequence complete ===")

if __name__ == "__main__":
    main()
