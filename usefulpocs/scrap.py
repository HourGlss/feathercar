import digitalio
import board
import busio
import adafruit_mcp2515

cs = digitalio.DigitalInOut(board.CAN_CS)
cs.switch_to_output()
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
matches = [
            adafruit_mcp2515.Match(0x060, mask = 0x7F0)
        ]
# for me, the first 3 bits correspond to priority
# the next 4 bits are used for the device number
# the last 4 correspond to the message type.
# each device except the central controller can then only need to listen to a subset of matches that correspond to it's
# device number

mcp = adafruit_mcp2515.MCP2515(spi, cs, baudrate=1000000)
received_messages = []
while True:
    # If there's a better way to specify mask, let me know.
    with mcp.listen(matches, timeout=.00001) as listener:
        next_message = listener.receive()
        while next_message is not None:
            received_messages.append(next_message)
            print("adding message")
            next_message = listener.receive()
     # just to prove the point
    while len(received_messages) > 0:
        received_messages.pop()