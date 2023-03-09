'''
ESC204S 2023 Lab 6, Task F
Task: Run a servo using the L298N driver.
'''
# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Servo standard servo example"""
import time
import board
import pwmio
from adafruit_motor import servo

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.GP16, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

while True:
    # 0 - 180 degrees, 5 degrees at a time.
    print('Rotating to 180')
    for angle in range(0, 180, 5):
        my_servo.angle = angle
        time.sleep(0.05)
    # 180 - 0 degrees, 5 degrees at a time.
    print('Rotating to 0')
    for angle in range(180, 0, -5):
        my_servo.angle = angle
        time.sleep(0.05)
