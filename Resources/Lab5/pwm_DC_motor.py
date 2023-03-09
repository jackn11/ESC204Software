'''
ESC204S 2023 Lab 6, Task D
Task: Use PWM to modulate the speed of a DC motor.
'''
import board
import time
import digitalio
import pwmio

# set up direction pins as digital outputs
in1 = digitalio.DigitalInOut(board.A1)
in2 = digitalio.DigitalInOut(board.A2)
in1.direction = digitalio.Direction.OUTPUT
in2.direction = digitalio.Direction.OUTPUT

# set up LED as PWM output
ena = pwmio.PWMOut(board.A0, duty_cycle = 0)

# set time limits
start_time = time.time()
time_limit = 10

# set starting (fastest) motor duty cycles
CW_duty = 25000
CCW_duty = 60000
duty_step = 5000
max_int = 65535

# rotate motor shaft in alternating directions with decreasing speed
while True:
    # rotate clockwise
    in1.value, in2.value = (False, True)
    ena.duty_cycle = CW_duty
    print("Rotating CW at %f duty cycle"%(100*CW_duty/max_int))
    CW_duty = CW_duty - duty_step
    time.sleep(2)

    # rotate counterclockwise
    in1.value, in2.value = (True, False)
    ena.duty_cycle = CCW_duty
    print("Rotating CCW at %f duty cycle"%(100*CCW_duty/max_int))
    CCW_duty = CCW_duty - duty_step
    time.sleep(2)

    # stop if time limit reached
    if time.time() - start_time > time_limit:
        break
