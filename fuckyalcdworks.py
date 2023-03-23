'''
ESC204 2023S Lab 2 Task D
Task: Light up onboard LED on button press.
'''
"""
# Import libraries needed for blinking the LED
import board
import digitalio

# Configure the internal GPIO connected to the LED as a digital output
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Configure the internal GPIO connected to the button as a digital input
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set the internal resistor to pull-up

# Print a message on the serial console
print('Hello! My LED is controlled by the button.')

# Loop so the code runs continuously
while True:
	led.value = True# if the button is pressed
"""


#gptbing
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Define the pins for the LCD.
lcd_rs = digitalio.DigitalInOut(board.GP2)
lcd_en = digitalio.DigitalInOut(board.GP3)
lcd_d4 = digitalio.DigitalInOut(board.GP18)
lcd_d5 = digitalio.DigitalInOut(board.GP19)
lcd_d6 = digitalio.DigitalInOut(board.GP20)
lcd_d7 = digitalio.DigitalInOut(board.GP21)

# Initialize the LCD class.
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# Print a message to the LCD.
lcd.message = "Hello, CircuitPy\nthon!"
