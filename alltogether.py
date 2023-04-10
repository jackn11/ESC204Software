
# FUNCTIONS TO PROCESS AND DISPLAY DATA
# data_to_display is string array
# returns when detects button press

def parse_csv():
    with open("/sd/data.txt", "r") as f:
        lines = f.readlines()
        headers = lines[0].strip().split(',')
        data = {header: [] for header in headers}
        for line in lines[1:]:
            values = line.strip().split(',')
            for i, value in enumerate(values):
                data[headers[i]].append(float(value))
    return data

def process_data():
    data = parse_csv()
    avg_temp = round(sum(data["temperature"])/len(data["temperature"]), 2)
    min_soil_ind = data["soilmoisture"].index(min(data["soilmoisture"]))
    min_soil_lat = data["latitude"][min_soil_ind]
    min_soil_long = data["longitude"][min_soil_ind]

    if sum(data["humidity"])/len(data["humidity"]) > 25:
        if sum(data["photoresistor"])/len(data["photoresistor"]) > 700:
            ideal_crop = "coffee"
        else:
            ideal_crop = "maize"
    else:
        ideal_crop = "cassava"

    return ["yield est (kg): "+str(avg_temp), "water soil at: ("+str(min_soil_lat)+", "+str(min_soil_long)+")", "ideal crop to grow: "+ideal_crop]

def display_info(data_arr, button, prev, down_up, button2):
    
    # Processing screen
    lcd.message = ("Processing...          \n                ")
    time.sleep(0.5)
    
    # BUTTON 2
    # Set variable prev to be the initial button value to keep track of current button state
    prev2 = button2.value
    # Initialize variable down_up to be True, this keeps track of whether or not the button has been pressed and released
    down_up2 = False
    # initialize state
    state = 0
    
    flag = False



    while True:
        # BUTTON 1
        # Set variable cur to be the current button value at that given moment
        cur = button.value
        # If cur does not equal prev, there has been a change of the button state
        if cur != prev:
            # If cur is False, that means the button is currently down, meaning the button has been pressed
            if not cur:
                down_up = False # The down_up variable is set to False, as the press-release pattern has not yet been detected
            # If cur is True, that means the button is currently up, meaning the button has been released after a press
            else:
                down_up = True # In this else block, prev = False and cur = True, meaning the button has been pressed and has just been released, so we set down_up to be True

        prev = cur

        if len(data_arr[state]) >= 16 and flag == False:
            print_long_message(data_arr[state])
            flag = True
        elif len(data_arr[state]) >= 16 and flag == True:
            lcd.message = str(data_arr[state][-16:] + "\n                ")
        else:
            lcd.message = str(data_arr[state])

        #BUTTON 2
        # Set variable cur to be the current button value at that given moment
        cur2 = button2.value
        # If cur does not equal prev, there has been a change of the button state
        if cur2 != prev2:
            # If cur is False, that means the button is currently down, meaning the button has been pressed
            if not cur2:
                down_up2 = False # The down_up variable is set to False, as the press-release pattern has not yet been detected
            # If cur is True, that means the button is currently up, meaning the button has been released after a press
            else:
                down_up2 = True # In this else block, prev = False and cur = True, meaning the button has been pressed and has just been released, so we set down_up to be True
                if state != (len(data_arr)-1):
                    state += 1
                    flag = False
                else:
                    state = 0
                    flag = False
        prev2 = cur2
        
        
        if down_up2 and len(data_arr[state]) >= 16 and flag == False:
            print_long_message(data_arr[state])
            flag = True
        elif down_up2 and len(data_arr[state]) >= 16 and flag == True:
            lcd.message = str(data_arr[state][-16:] +"\n                ")
        elif down_up2:
            lcd.message = str(data_arr[state])
        else:
            pass
        

        if down_up:
            return
            
        


def print_long_message(message):
    x = 0
    y = 16
    
    for i in range(0, len(message)-16):
        x = i
        lcd.message = (message[x:y] + "\n                ")
        y += 1
        time.sleep(0.5) # Increase the sleep time to slow down the scroll speed
        
    
    # Display the remainder of the message
    lcd.message = (message[x:] + " \n          ")
    
    return
        


# Jack Naimer AND BENJAMIN MAH :)

import adafruit_character_lcd.character_lcd as characterlcd


# all 4 work together

#DHT SENSOR
import board
import bitbangio
import adafruit_am2320
import time

#GPS
import adafruit_gps
import busio

# SD card testing
import adafruit_sdcard
import digitalio
import storage

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.GP6, board.GP7, board.GP4) #sck, mosi, miso
cs = digitalio.DigitalInOut(board.GP5)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Create a file in write mode and write something
with open("/sd/data.txt", "w") as file:
    file.write("temperature,humidity,photoresistor,soilmoisture,latitude,longitude,altitude,year,month,day,hour\r\n")

RX = board.GP1
TX = board.GP0

uart = busio.UART(TX, RX, baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()



#PHOTORESISTOR
import analogio
# set display to show either ADC output representative integer or
# the voltage that it represents
INT_MODE = 0
VOLT_MODE = 1
mode = INT_MODE
# always 0xff (in hex) according to: https://learn.adafruit.com/
# circuitpython-basics-analog-inputs-and-outputs/
# analog-to-digital-converter-inputs
ADC_HIGH = 65535
# set up photoresistor as analog input over analog pin A0
# (on GPIO pin 26 for Pico, needs to be changed if using Nano)
photoresistor_pin = board.GP26_A0
photoresistor = analogio.AnalogIn(photoresistor_pin)
# show reference voltage (logic high, 3.3V) and the
# corresponding analog integer value
ADC_REF = photoresistor.reference_voltage
print("ADC reference voltage: {}".format(ADC_REF))
print("ADC high voltage integer value: {}".format(ADC_HIGH))
print('=' * 40)  # Print a separator line.
print("DATA ACQUISITION START")
# convert ADC input value back to voltage
def adc_to_voltage(adc_value):
    return  ADC_REF * (float(adc_value)/float(ADC_HIGH))


#SOIL MOISTURE
# use variables instead of numbers:
  # 0  ~300     dry soil
  # 300~700     humid soil
  # 700~950     in water
soil = board.GP27_A1 # Soil moisture PIN reference
soil_value = analogio.AnalogIn(soil)



# set up I2C protocol
i2c = bitbangio.I2C(board.GP17, board.GP16)
dhtDevice = adafruit_am2320.AM2320(i2c)


#the good stuffs
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Define the pins for the LCD.
lcd_rs = digitalio.DigitalInOut(board.GP2) #GP2
lcd_en = digitalio.DigitalInOut(board.GP3) #GP3
lcd_d4 = digitalio.DigitalInOut(board.GP18) #GP18
lcd_d5 = digitalio.DigitalInOut(board.GP19) #19
lcd_d6 = digitalio.DigitalInOut(board.GP20) #20
lcd_d7 = digitalio.DigitalInOut(board.GP21) #21

# Initialize the LCD class.
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

'''
# Print a message to the LCD.
lcd.message = "TEST"
lcd.message = "Hello, CircuitPy\nthon!"
# end of good stuff
'''


# BUTTON 1 - TO STOP COLLECTING DATA AND MOVE TO PROCESS DATA FUNCTION
# Assing internal GPIO as button input
button = digitalio.DigitalInOut(board.GP11)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Configure the internal resistor to pull-up
# Set variable prev to be the initial button value to keep track of current button state
prev = button.value
# Initialize variable down_up to be True, this keeps track of whether or not the button has been pressed and released
down_up = False


# BUTTON 2 - TO CYCLE THROUGH PROCESSED DATA, WILL BE USED IN DISPLAY INFO FUNCTION
# Assing internal GPIO as button input
button2 = digitalio.DigitalInOut(board.GP12)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP # Configure the internal resistor to pull-up


# read values from AM2320 sensor every 2 seconds
# (with gap in between temp and humidity readings)

# loading counter
counter = 0
while True:

    if counter == 2:
        counter = 0
    else:
        counter += 1

    # KEEP TRACK OF TIME FOR SENSOR SO IT DOESN'T COLLECT EVERY SINGLE MILLISECOND
    #start_time = time.monotonic()

    # BUTTON 1
    # Set variable cur to be the current button value at that given moment
    cur = button.value
    # If cur does not equal prev, there has been a change of the button state
    if cur != prev:
        # If cur is False, that means the button is currently down, meaning the button has been pressed
        if not cur:
            down_up = False # The down_up variable is set to False, as the press-release pattern has not yet been detected
        # If cur is True, that means the button is currently up, meaning the button has been released after a press
        else:
            down_up = True # In this else block, prev = False and cur = True, meaning the button has been pressed and has just been released, so we set down_up to be True
    prev = cur

    if down_up:
        down_up = False
        display_info(process_data(), button, prev, down_up, button2)

    if counter == 0:
        lcd.message = str("Collecting      \nData.      ")
    elif counter == 1:
        lcd.message = str("Collecting      \nData..     ")
    else:
        lcd.message = str("Collecting      \nData...    ")




    # if button_pressed:
    #	data_to_display = process_data() # string array
    #	display_info(data_to_display)


    print('=' * 40)  # Print a separator line.



    gps_is_plugged_in = True

    if gps_is_plugged_in:
        gps.update()
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            if not gps.has_fix:
                print('Waiting for fix...')
                continue

            latitude = gps.latitude
            longitude = gps.longitude
            altitude = gps.altitude_m
            #these next couple lines may be sketch
            year = gps.timestamp_utc.tm_year
            month = gps.timestamp_utc.tm_mon
            day = gps.timestamp_utc.tm_mday
            hour = gps.timestamp_utc.tm_hour

            print('Latitude: {0:.6f} degrees'.format(gps.latitude))
            print('Longitude: {0:.6f} degrees'.format(gps.longitude))
            print('Altitude: {} meters'.format(gps.altitude_m))
            print('Speed: {} knots'.format(gps.speed_knots))
            print('Heading: {} degrees'.format(gps.track_angle_deg))
            print('Timestamp: {}'.format(gps.timestamp_utc))
    else:
        lattitude,longitude,altitude,year,month,day,hour = 43.65, -79.39, 87.3, 2023, 3, 14, 15


    try:
        # Print the values to the serial port
        temp_c = dhtDevice.temperature
        time.sleep(0.5)
        hum = dhtDevice.relative_humidity
        print("AM2320 Temp: {:.1f}C \nHumidity: {}% ".format(temp_c,hum))

    except RuntimeError as error:
		# Errors happen fairly often, DHTs are hard to read,
        # just keep trying to run/power cycle Pico
        # If errors are persistent, increase sleep times
        # Replacing bitbangio with busio can also sometimes help
        print(error.args[0])



    # PHOTORESISTOR STUFF
    # read adc value and print
    if mode == INT_MODE:
        print("Photoresistor value:", photoresistor.value)
    # convert to voltage
    else:
        print((adc_to_voltage(photoresistor.value),))



    # SOIL MOISTURE
    moisture = soil_value.value
    print("Soil Moisture Value:", moisture)



    # SOIL MOISTURE
    if moisture <= 300:
        print("Soil is dry!")
    elif moisture <= 700:
        print("Soil is moist!")
    else:
        print("Soil is in water/wet!")



    # WRITE TO SD CARD
    # Append information to a file
    with open("/sd/data.txt", "a") as file:
        file.write("{},{},{},{},{},{},{},{},{},{},{}\r\n".format(temp_c,hum,photoresistor.value,moisture,lattitude,longitude,altitude,year,month,day,hour))
    time.sleep(0.1)





'''
# Open the file in read mode and read from it
with open("/sd/sdtest.txt", "r") as file:
    data = file.read()
    print(data)
'''
