from math import floor
import board
import busio
import digitalio
from adafruit_rplidar import RPLidar
print("LIDAR")
uart = busio.UART(
    tx=board.TX,
    rx=board.RX,
    parity=busio.UART.Parity.EVEN,
    stop=1,
    baudrate=115200)
motor_pin = digitalio.DigitalInOut(board.D4)
motor_pin.direction = digitalio.Direction.OUTPUT
motor_pin.value = False
lidar = RPLidar(motor_pin, port=uart, timeout=3,logging=True)

# used to scale data to fit on the screen
max_distance = 0


def process_data(data):
    print(data)


scan_data = [0] * 360

try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for _, angle, distance in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

except KeyboardInterrupt:
    print("Stopping.")
lidar.stop()
lidar.disconnect()