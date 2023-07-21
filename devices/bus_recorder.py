from __future__ import annotations

#
# THIS IS DEVICE 3
#
DEVICE = 8

import board
import sys
import os
import time
import busio
import digitalio
import storage
import sdcardio
from adafruit_mcp2515 import MCP2515 as CAN

# CAN MESSAGE AND ICD IMPORTS
try:
    from canmessage import CanMessage
except:
    try:
        from can_info.canmessage import CanMessage
    except:
        print("Can lib not found")


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


spi = busio.SPI(board.D6, board.SCL, board.TX)
sdcard = sdcardio.SDCard(spi, board.D5)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
can = CANBus()
print("worked")
while True:
    cm = CanMessage(DEVICE)
    cm.encode_data(1, number=7)
    can_bus.send(cm)
