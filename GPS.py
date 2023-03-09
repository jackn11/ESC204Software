import board
import busio
import adafruit_gps
import time

# Set up UART serial communication with the GPS module
uart = busio.UART(board.GP0, board.GP1, baudrate=9600, timeout=10)

# Create a GPS object
gps = adafruit_gps.GPS(uart)

# Turn on the basic GGA and RMC info (no need for other messages)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

# Main loop
while True:
    # Check if a GPS fix has been acquired
    if gps.has_fix:
        # Print out GPS data
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        print('Altitude: {} meters'.format(gps.altitude_m))
        print('Speed: {} knots'.format(gps.speed_knots))
        print('Heading: {} degrees'.format(gps.track_angle_deg))
        print('Timestamp: {}'.format(gps.timestamp_utc))
    else:
        print('Waiting for fix...')

    # Wait a bit before checking again
    time.sleep(1.0)
