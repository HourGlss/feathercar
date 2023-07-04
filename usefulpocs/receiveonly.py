import digitalio
import board
import busio
from adafruit_mcp2515.canio import Timer
from adafruit_mcp2515.canio import RemoteTransmissionRequest, Message
from adafruit_mcp2515 import MCP2515 as CAN

cs = digitalio.DigitalInOut(board.CAN_CS)
cs.switch_to_output()
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
mcp = CAN(spi, cs, baudrate=1000000)
next_message = None
message_num = 0
while True:
    message_count = mcp.unread_message_count
    message_num = 0
    next_message = mcp.read_message()
    while next_message is not None:
        message_num += 1
        msg = next_message
        next_message = mcp.read_message()
