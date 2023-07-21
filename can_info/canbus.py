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
    next_message_to_send: None | CanMessage
    received_messages: list

    def __init__(self, device):
        self.next_massage_to_send = None
        self.device = device
        self.create_bus_connection()
        self.received_messages = []

    def create_bus_connection(self):
        cs = digitalio.DigitalInOut(board.CAN_CS)
        cs.switch_to_output()
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.mcp = None
        self.mcp = CAN(spi, cs, baudrate=1000000)
        assert self.mcp is not None

    def create_message(self, message_number, **kwargs):
        cm = CanMessage(self.device)
        self.next_massage_to_send = cm.encode_data(message_number, **kwargs)

    def send(self):
        self.next_massage_to_send: CanMessage = self.next_message_to_send
        self.mcp.send(self.next_massage_to_send.msg)
        self.next_massage_to_send = None

    def listen(self):
        with self.mcp.listen(timeout=.001) as listener:
            next_message = listener.receive()
            while next_message is not None:
                self.received_messages.append(next_message)
                next_message = listener.receive()

