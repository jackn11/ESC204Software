# Write your code here :-)
'''
ESC204S 2023 Lab 6, Task B
Task: Use PWM to modulate the brightness of an LED.
'''
import board
import pwmio
import time

# set up LED as PWM output
led = pwmio.PWMOut(board.A0, frequency=100, duty_cycle=0)

# run PWM
while True:
    for duty in range(0,65535,50):
        # increasing duty cycle
        led.duty_cycle = duty# Up
        time.sleep(0.001)

    for duty in range(65535,0,-50):
        # decreasing duty cycle
        led.duty_cycle = duty# Up
        time.sleep(0.001)
