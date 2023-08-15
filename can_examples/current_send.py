import time
import board
import busio
import digitalio
from adafruit_mcp2515.canio import Message, RemoteTransmissionRequest
from adafruit_mcp2515 import MCP2515 as CAN
def print_status(msg):
    l = len(msg)
    header = "=" * (l + 4)
    print(header)
    to_send = f"-- {msg:>}"
    print(to_send)
print_status("MASTER MODULE")
print_status("Imports done")
class CANConnection:

    def __init__(self):
        cs = digitalio.DigitalInOut(board.CAN_CS)
        cs.switch_to_output()
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.mcp = CAN(spi, cs, baudrate=1000000)
can = CANConnection()
print_status("Waiting for SLAVE to turn on")
time.sleep(3)
current_can_id = 1
max_can_id = 0x7FF
print_status("SENDING")
while True:
    '''
    with can.mcp.listen() as listener:
        message_count = listener.in_waiting()
        for _i in range(message_count):
            msg = listener.receive()
            if isinstance(msg, Message):
                #print("message data:", msg.data)
                pass
            if isinstance(msg, RemoteTransmissionRequest):
                # print("RTR length:", msg.length)
                pass
            if msg is not None and msg.id == 0x7FE:
                print(msg.data)
    '''
    message = Message(current_can_id, data=b'deadbeef')
    current_can_id += 1
    send_success = can.mcp.send(message)
    print(current_can_id)
    if current_can_id == max_can_id:
        current_can_id = 1