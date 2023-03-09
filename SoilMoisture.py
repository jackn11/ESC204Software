# Import libraries to allow microcontroller and breadboard functionality
import board
import time
import analogio

# use variables instead of numbers:
soil = board.GP26_A0 # Soil moisture PIN reference
soil_value = analogio.AnalogIn(soil)

while True:
    moisture = soil_value.value
    print(moisture)
    time.sleep(0.5)# set a delay between readings
