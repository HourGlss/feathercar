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

import pwmio

steering_pwm = pwmio.PWMOut(board.D5, frequency=50)
throttle_pwm = pwmio.PWMOut(board.D25, frequency=50)


def normalize(value, type_of_movement):
    bounds = {"steering": {
        "desired": {
            "lower": 4000,
            "upper": 6000
        },
        "actual": {
            "lower": -100,
            "upper": 100
        }
    },
        "throttle":
            {
                "desired": {
                    "lower": 3000,
                    "upper": 7000
                },
                "actual": {
                    "lower": -100,
                    "upper": 100
                }
            }
    }

    return int(bounds[type_of_movement]['desired']['lower'] + (value - bounds[type_of_movement]['actual']['lower']) * (bounds[type_of_movement]['desired']['upper'] - bounds[type_of_movement]['desired']['lower']) / (bounds[type_of_movement]['actual']['upper'] - bounds[type_of_movement]['actual']['lower']))



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


can = CANBus()
steering_value = 0
throttle_value = 0
while True:
    with can.mcp.listen(timeout=1.0) as listener:
        message_count = listener.in_waiting()

        next_message = listener.receive()
        while not next_message is None:
            # print(next_message.data)
            cm = CanMessage(DEVICE, next_message)
            if cm.decode_data():
                # print(cm.msg.data)
                steering_value = cm.parsed_data['steering']
                throttle_value = cm.parsed_data['throttle']
                throttle_value *= -1
                steering_pwm.duty_cycle = normalize(steering_value,"steering")
                throttle_pwm.duty_cycle = normalize(throttle_value, "throttle")
            else:
                print("decode failure")
                sys.exit()
            next_message = listener.receive()
