from __future__ import annotations

from adafruit_mcp2515 import MCP2515 as CAN
import board
import digitalio
import busio

try:
    from canmessage import CanMessage
except:
    try:
        from can_info.canmessage import CanMessage
    except:
        print("Can lib not found")


class CANBus:
    mcp: None | CAN

    def __init__(self,device):
        self.device = device
        self.create_bus_connection()

    def create_bus_connection(self):
        cs = digitalio.DigitalInOut(board.CAN_CS)
        cs.switch_to_output()
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.mcp = None
        self.mcp = CAN(spi, cs, baudrate=1000000)
        assert self.mcp is not None

    def create_message(self,message_number, **kwargs):
