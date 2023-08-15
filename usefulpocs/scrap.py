# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import board
import time
import digitalio
import busio
from math import floor
from zxc import RPLidar

# Setup the RPLidar
uart = busio.UART(
    tx=board.TX,
    rx=board.RX,
    baudrate=115200)
motor_control = digitalio.DigitalInOut(board.D4)
motor_control.switch_to_output()
lidar = RPLidar(motor_control, uart, timeout=3)

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
        print(scan_data)

except KeyboardInterrupt:
    print("Stopping.")
lidar.stop()
lidar.disconnect()