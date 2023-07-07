from __future__ import annotations

import board
import sys
#
# THIS IS DEVICE 2
#
DEVICE = 2
# ACTUAL CAN BUS IMPORTS
import time
import busio
import digitalio
from adafruit_mcp2515 import MCP2515 as CAN
# CAN MESSAGE AND ICD IMPORTS
try:
    from canmessage import CanMessage
except:
    try:
        from can_info.canmessage import CanMessage
    except:
        print("Can lib not found")
from icd import icd

import pwmio
pwm = pwmio.PWMOut(board.D5, frequency=5000, duty_cycle=20000)

print("imports are good")
STEERING_MIN = 950  # Minimum pulse width for full left position
STEERING_MAX = 1850  # Maximum pulse width for full right position

def set_servo_angle(angle):
    print(angle)
    pulse_width = int(STEERING_MIN + ((angle + 100) / 200) * (STEERING_MAX - STEERING_MIN))
    pwm.duty_cycle = pulse_width

class CANBus:
    mcp: None | CAN

    def __init__(self):
        cs = digitalio.DigitalInOut(board.CAN_CS)
        cs.switch_to_output()
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.mcp = None
        try:
            self.mcp = CAN(spi, cs, baudrate=1000000)
        except:
            print("CAN BUS CANNOT BE MADE")


print("class creation is good")

can = CANBus()

print("class instantiation is done")
# steering_value = 0
# throttle_value = 0
# while True:
#     with can.mcp.listen(timeout=1.0) as listener:
#         message_count = listener.in_waiting()
#
#         next_message = listener.receive()
#         while not next_message is None:
#             # print(next_message.data)
#             cm = CanMessage(DEVICE, next_message)
#             if cm.decode_data():
#                 # print(cm.msg.data)
#                 steering_value = cm.parsed_data['steering']
#                 throttle_value = cm.parsed_data['throttle']
#                 # print(steering_value, throttle_value)
#             else:
#                 print("decode failure")
#                 sys.exit()
#             next_message = listener.receive()
while True:
    # Move the servo to the left
    set_servo_angle(-100)  # -100 corresponds to full left position
    time.sleep(1)  # Wait for 1 second

    # Move the servo to the right
    set_servo_angle(100)  # 100 corresponds to full right position
    time.sleep(1)  # Wait for 1 second