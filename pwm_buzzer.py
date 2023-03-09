'''
ESC204S 2023 Lab 6, Task C
Task: Use PWM to modulate the volume (and frequency) of a buzzer noise.
'''
import board
import pwmio
import time

# set up buzzer as PWM output
buzzbuzz = pwmio.PWMOut(board.A0, duty_cycle = 5000, frequency = 440, variable_frequency = True)

# set mode
mode = "duty"
#mode = "freq"

# run PWM while changing either duty cycle or frequency
while True:
    # cycle up and down through duty cycle values
    if mode == "duty":
        for duty in range(0,40000,buzzbuzz.duty_cycle):
            # increasing duty cycle
            buzzbuzz.duty_cycle = duty
            time.sleep(0.1)
            buzzbuzz.duty_cycle = 0
            time.sleep(0.01)

        for duty in range(40000,0,-buzzbuzz.duty_cycle):
            # decreasing duty cycle
            buzzbuzz.duty_cycle = duty
            time.sleep(0.1)
            buzzbuzz.duty_cycle = 0
            time.sleep(0.01)

    elif mode == "freq":
        # cycle up and down through frequency values
        for f in range(50,700,50):
            # increasing duty cycle
            buzzbuzz.frequency = f# Up
            time.sleep(0.1)

        for f in range(700,50,-50):
            # decreasing duty cycle
            buzzbuzz.frequency = f# Down
            time.sleep(0.1)
