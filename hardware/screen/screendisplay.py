# display.py
# SSD1306 OLED display functions for catapult status messages.
# 128x64 pixel display over I2C.

from machine import Pin, I2C
import ssd1306
import framebuf
import config

# ═══════════════════════════════════════════════════════════
# HARDWARE SETUP
# ═══════════════════════════════════════════════════════════

def init_display():
    """
    Initialise the SSD1306 OLED display over I2C.
    Returns the display object.
    Raises OSError if display is not found — check SDA/SCL wiring.
    """
    try:
        i2c  = I2C(config.DISPLAY_I2C_ID,
                   scl=Pin(config.DISPLAY_SCL),
                   sda=Pin(config.DISPLAY_SDA),
                   freq=400_000)
        oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        oled.fill(0)
        oled.show()
        print("Display initialised.")
        return oled
    except OSError as e:
        raise OSError(
            f"Display init failed — check wiring "
            f"(SDA=GP{config.DISPLAY_SDA}, SCL=GP{config.DISPLAY_SCL}): {e}"
        )

# ═══════════════════════════════════════════════════════════
# TEXT HELPER
# ═══════════════════════════════════════════════════════════

def _big_text(oled, text, x, y, scale=2):
    """
    Draw scaled up text on the display.
    scale=2 doubles the size, scale=3 triples it.
    At scale=2: ~8 characters fit per line.
    At scale=3: ~5 characters fit per line.
    """
    buf = bytearray(len(text) * 8 * 8)
    fb  = framebuf.FrameBuffer(buf, len(text) * 8, 8, framebuf.MONO_HLSB)
    fb.text(text, 0, 0, 1)
    for row in range(8):
        for col in range(len(text) * 8):
            if fb.pixel(col, row):
                oled.fill_rect(
                    x + col * scale,
                    y + row * scale,
                    scale, scale, 1
                )

# ═══════════════════════════════════════════════════════════
# STATUS SCREENS
# ═══════════════════════════════════════════════════════════

def show_scanning(oled):
    """
    Displayed during the scan phase.
    """
    oled.fill(0)
    _big_text(oled, "Scanning", 0, 10, scale=2)
    _big_text(oled, "...",      0, 36, scale=2)
    oled.show()

def show_target_found(oled, distance_mm):
    """
    Displayed when the nearest target is identified.
    Shows the angle and distance of the target.
    """
    oled.fill(0)
    _big_text(oled, "Target",  0, 0,  scale=2)
    _big_text(oled, "Found!",  0, 18, scale=2)
    oled.text(f"{distance_mm:.0f} mm", 0, 54, 1)
    oled.show()

def show_target_destroyed(oled):
    """
    Displayed after the shot is complete.
    """
    oled.fill(0)
    _big_text(oled, "Target",    0, 0,  scale=2)
    _big_text(oled, "Destroyed", 0, 20, scale=1)
    _big_text(oled, "!!!",       32, 44, scale=2)
    oled.show()

def show_target_not_found(oled):
    """
    Displayed after scanning if no object is found
    """

    oled.fill(0)
    _big_text(oled, "Target",    0, 0,  scale=2)
    _big_text(oled, "Not", 0, 20, scale=1)
    _big_text(oled, "Found :(",       32, 44, scale=2)
    oled.show()

def show_firing(oled):
    """Displayed each time the catapult fires."""
    oled.fill(0)
    _big_text(oled, "Firing", 0, 10, scale=2)
    oled.show()