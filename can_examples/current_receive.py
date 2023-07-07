import board
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode
import time
import digitalio
import busio
import pwmio
from adafruit_mcp2515.canio import Timer
from adafruit_mcp2515.canio import RemoteTransmissionRequest, Message
from adafruit_mcp2515 import MCP2515 as CAN


class CAN_connection:

    def __init__(self):
        cs = digitalio.DigitalInOut(board.CAN_CS)
        cs.switch_to_output()
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.mcp = CAN(spi, cs, baudrate=1000000)



class LargeLcd:
    lcd: LCD
    i2c: board.I2C
    current_pos = 0

    def __init__(self):

        try:
            self.i2c = board.I2C()
        except RuntimeError:
            self.i2c = None
            print("LCD not connected?")
        self.i2c_address = 0x27
        self.num_rows = 4
        self.num_cols = 20
        self.lcd = self.create_lcd()

    def create_lcd(self):
        if self.i2c is None:
            return None
        this_lcd = LCD(
            I2CPCF8574Interface(self.i2c, self.i2c_address),
            num_rows=self.num_rows,
            num_cols=self.num_cols)
        this_lcd.set_cursor_pos(0, 0)
        this_lcd.print("test good")

        return this_lcd

    def print(self, data):
        if not isinstance(data,Message):
            data_to_print = f"{data}"
        else:
            data_to_print = f'{data.id} {data.data.decode("utf-8")}'

        if self.lcd is None:
            print(data_to_print)
        else:
            self.lcd.set_cursor_pos(self.current_pos, 0)
            self.lcd.print(data_to_print)
            self.current_pos = (self.current_pos + 1) % 4


print("starting")
lcd = LargeLcd()
can = CAN_connection()


next_message = None
message_num = 0
while True:
    message_count = can.mcp.unread_message_count
    message_num = 0
    next_message = can.mcp.read_message()
    while next_message is not None:
        message_num += 1
        msg = next_message
        lcd.print(msg)
        next_message = can.mcp.read_message()