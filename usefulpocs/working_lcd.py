import board

from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

from lcd.lcd import CursorMode
import time
# Talk to the LCD at I2C address 0x27.
# The number of rows and columns defaults to 4x20, so those
# arguments could be omitted in this case.
# https://github.com/dhalbert/CircuitPython_LCD/tree/main
lcd = LCD(I2CPCF8574Interface(board.I2C(), 0x27), num_rows=4, num_cols=20)
lcd.set_cursor_pos(0, 0)
lcd.print("0zzz456789abcdefghij")


time.sleep(20)
