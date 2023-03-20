# all 4 work together

#DHT SENSOR
import board
import bitbangio
import adafruit_am2320
import time

#GPS
import adafruit_gps
import busio

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

# read values from AM2320 sensor every 2 seconds
# (with gap in between temp and humidity readings)
while True:

    gps.update()

    print('=' * 40)  # Print a separator line.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...')
            continue
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        print('Altitude: {} meters'.format(gps.altitude_m))
        print('Speed: {} knots'.format(gps.speed_knots))
        print('Heading: {} degrees'.format(gps.track_angle_deg))
        print('Timestamp: {}'.format(gps.timestamp_utc))


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

    time.sleep(3.0)


'''
# SD card testing
import adafruit_sdcard
import busio
import digitalio
import board
import storage

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.GP6, board.GP7, board.GP4)
cs = digitalio.DigitalInOut(board.GP5)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Create a file in write mode and write something
with open("/sd/sdtest.txt", "w") as file:
    file.write("Hello World!\r\n")
    file.write("This is a test\r\n")

# Open the file in read mode and read from it
with open("/sd/sdtest.txt", "r") as file:
    data = file.read()
    print(data)
'''
