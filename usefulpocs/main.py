import board
import busio
import time
from digitalio import DigitalInOut
import neopixel
from adafruit_mcp2515.canio import Message
from adafruit_mcp2515 import MCP2515 as CAN

board.board_id = "adafruit_feather_rp2040_can"

def set_light_blue():
    pixel.fill((0, 0, 255))


def set_light_red():
    pixel.fill((255, 0, 0))


pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

pixel.brightness = 1

cs = DigitalInOut(board.D5)
cs.switch_to_output()
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

can_bus = CAN(spi, cs, baudrate=1000000)  # use loopback to test without another device
message = Message(id=0x1234ABCD, data=b"adafruit", extended=True)
while True:
    set_light_blue()
    send_success = can_bus.send(message)
    # print("Send success:", send_success)
    set_light_red()
