# Catapult Project
An autonomous targeting and launching system powered by the **Raspberry Pi Pico 2** and **MicroPython**.

## Hardware Components
* **Microcontroller:** Raspberry Pi Pico 2 (RP2350)
* **Distance Sensor:** VL53L0X Time-of-Flight laser ranging sensor (I2C interface)
* **Actuator:** NEMA 17 Stepper Motor / MG90S Micro Servo / MG996R 360 servo
 * **Display Screen:** OLED display module
 * **Motor Driver:** DRV8825 Stepper Driver

## 💻 Software Setup
1. Flash the latest **MicroPython** UF2 firmware to your Pico 2.
2. Install the `vl53l0x` library via mpremote or Thonny.
3. Upload `main.py` and your hardware abstraction classes.


## Process
1. Scan → find target
2. Calculate flap angle
3. Stepper rotates to target angle
4. MG996R sets flap angle
5. Start flywheel
6. Wait (e.g. 2000ms) for it to spin up
7. MG90S opens hatch → ball drops in
8. Wait briefly
9. MG90S closes hatch
10. Stop flywheel