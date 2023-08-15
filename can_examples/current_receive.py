import board
import time
import digitalio
import busio
from adafruit_mcp2515.canio import Timer
from adafruit_mcp2515.canio import RemoteTransmissionRequest, Message
from adafruit_mcp2515 import MCP2515 as CAN




def print_status(msg):
    l = len(msg)
    header = "=" * (l + 4)
    print(header)
    to_send = f"-- {msg:>}"
    print(to_send)

print_status("SLAVE MODULE")
print_status("Imports done")
class CANConnection:

    def __init__(self):
        cs = digitalio.DigitalInOut(board.CAN_CS)
        cs.switch_to_output()
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.mcp = CAN(spi, cs, baudrate=1000000)


can = CANConnection()
print_status("Class creation done")

# next_message = None
# message_num = 0
# while True:
#     message_count = can.mcp.unread_message_count
#     message_num = 0
#     next_message = can.mcp.read_message()
#     while next_message is not None:
#         message_num += 1
#         msg = next_message
#         print(msg.id)
#         next_message = can.mcp.read_message()

while True:
    with can.mcp.listen(timeout=1.0) as listener:
        message_count = listener.in_waiting()
        # print(message_count, "messages available")
        for _i in range(message_count):
            msg = listener.receive()
            # print("Message from ", hex(msg.id))
            if isinstance(msg, Message):
                # print("message data:", msg.data)
                pass
            if isinstance(msg, RemoteTransmissionRequest):
                # print("RTR length:", msg.length)
                pass