import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Define the pins for the LCD.
lcd_rs = digitalio.DigitalInOut(board.GP16)
lcd_en = digitalio.DigitalInOut(board.GP17)
lcd_d4 = digitalio.DigitalInOut(board.GP18)
lcd_d5 = digitalio.DigitalInOut(board.GP19)
lcd_d6 = digitalio.DigitalInOut(board.GP20)
lcd_d7 = digitalio.DigitalInOut(board.GP21)

# Initialize the LCD class.
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# Print a message to the LCD.
lcd.message = "Hello, CircuitPy\nthon!"
