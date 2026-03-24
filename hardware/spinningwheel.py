from machine import Pin, PWM
import time
import config

motor = Pin(config.MOTOR1_PIN, Pin.OUT)
motor2 = Pin(config.MOTOR2_PIN, Pin.OUT)


def start_spinning_wheel():
    motor.value(1)
    motor2.value(1)
    time.sleep_ms(650)




def stop_spinning_wheel():        
    motor.value(0)
    motor2.value(0)

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