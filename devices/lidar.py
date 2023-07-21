# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

from math import floor
from adafruit_rplidar import RPLidar
import busio
import board
from digitalio import DigitalInOut, Direction, Pull

# Set up Motor Control GPIO
motor_control = DigitalInOut(board.D12)
motor_control.direction = Direction.OUTPUT

# Set up UART
uart = busio.UART(tx=board.TX, rx=board.RX, baudrate=115200, bits=8, parity=busio.UART.Parity.ODD, stop=1, timeout=1)

def process_data(data):
    print(data)


# Setup the RPLidar
lidar = RPLidar(motor_control, uart, 115200, 300,logging=True)
for k,v in lidar.info():
    print(k,v)
scan_data = [0] * 360

# try:
    #    )
#     for scan in lidar.iter_scans():
#         for _, angle, distance in scan:
#             scan_data[min([359, floor(angle)])] = distance
#         process_data(scan_data)
#
# except KeyboardInterrupt:
#     print("Stopping.")
lidar.stop()
lidar.disconnect()
