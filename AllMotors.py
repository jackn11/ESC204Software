# Write your code here :-)
import time
import board
import analogio
import digitalio
import pwmio

# Define the potentiometer and joystick pins
#pot_pin = board.GP27
joystick_x_pin = board.GP26
joystick_y_pin = board.GP28

# set up direction pins for lift motors
lift_motor1_in1 = digitalio.DigitalInOut(board.GP10)
lift_motor1_in2 = digitalio.DigitalInOut(board.GP11)
lift_motor1_in1.direction = digitalio.Direction.OUTPUT
lift_motor1_in2.direction = digitalio.Direction.OUTPUT

lift_motor2_in1 = digitalio.DigitalInOut(board.GP12)
lift_motor2_in2 = digitalio.DigitalInOut(board.GP13)
lift_motor2_in1.direction = digitalio.Direction.OUTPUT
lift_motor2_in2.direction = digitalio.Direction.OUTPUT

# set up motor driving signal as PWM output
lift_motor1_ena = pwmio.PWMOut(board.GP14, duty_cycle = 0)
lift_motor2_ena = pwmio.PWMOut(board.GP15, duty_cycle = 0)

# set up direction pins for horizontal motor
horz_motor_in1 = digitalio.DigitalInOut(board.GP8)
horz_motor_in2 = digitalio.DigitalInOut(board.GP9)
horz_motor_in1.direction = digitalio.Direction.OUTPUT
horz_motor_in2.direction = digitalio.Direction.OUTPUT

# set up motor driving signal as PWM output 
horz_motor_ena = pwmio.PWMOut(board.GP7, duty_cycle = 0)


# Set up the potentiometer and joystick pins as inputs
#pot = analogio.AnalogIn(pot_pin)
joystick_x = analogio.AnalogIn(joystick_x_pin)
joystick_y = analogio.AnalogIn(joystick_y_pin)


# Define a function to map the analog input value to a range of 0-255
def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Loop forever reading the joystick and potentiometer values
while True:

    # Read the potentiometer value and map it to a range of 0-255
    #pot_value = map_range(pot.value, 0, 65535, 0, 255)
    #print("Potentiometer value: ", pot_value)

    # Read the joystick x and y values and map them to a range of 0-255

    joystick_x_value = map_range(joystick_x.value, 0, 65535, 0, 1000)
    joystick_y_value = map_range(joystick_y.value, 0, 65535, 0, 1000)
    print("Joystick X value: ", joystick_x_value)
    print("Joystick Y value: ", joystick_y_value)

    if (joystick_x_value > 950):
        lift_motor1_in1.value, lift_motor1_in2.value = (False, True)
        lift_motor2_in1.value, lift_motor2_in2.value = (False, True)
    elif (joystick_x_value < 50):
        lift_motor1_in1.value, lift_motor1_in2.value = (True, False)
        lift_motor2_in1.value, lift_motor2_in2.value = (True, False)
    else:
        lift_motor1_in1.value, lift_motor1_in2.value = (False, False)
    
    if (joystick_y_value > 950):
        horz_motor_in1.value, horz_motor_in2.value = (False, True)
    elif (joystick_y_value < 50):
        horz_motor_in1.value, horz_motor_in2.value = (True, False)
    else:
        horz_motor_in1.value, horz_motor_in2.value = (False, False)


    # Read the joystick button value and print a message if it's pressed
    #if not joystick_button.value:
        #print("Joystick button pressed")

    # Tell motor to move based on x axis (lift motors)
    if (abs(joystick_x_value - 517) > 35):
        driving_duty_cycle = map_range(joystick_x.value, 0, 1000, 0, 65535)
        #print("Sending motor command:", driving_duty_cycle)
        lift_motor1_ena.duty_cycle = 50000
        lift_motor2_ena.duty_cycle = 50000
    else:
        lift_motor1_ena.duty_cycle = 0
        lift_motor2_ena.duty_cycle = 0
        
    # Tell motoro to move based on y axis (horizontal axis)
    if (abs(joystick_y_value - 517) > 35):
        driving_duty_cycle = map_range(joystick_y.value, 0, 1000, 0, 65535)
        print("Sending motor command:", driving_duty_cycle)
        horz_motor_ena.duty_cycle = 50000
    else:
        horz_motor_ena.duty_cycle = 0

    # Wait for a short delay before reading the values again
    time.sleep(0.1)
