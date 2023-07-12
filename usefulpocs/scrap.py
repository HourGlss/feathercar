

# board.SCK, board.MOSI, board.MISO)


# sd = sdcardio.SDCard(otherspi, board.D5)
# vfs = storage.VfsFat(sd)
# storage.mount(vfs, '/sd')
# print("sdcardio init passed")


#
# THIS IS DEVICE 3
#
DEVICE = 8
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
        cs = digitalio.DigitalInOut(board.CAN_CS)  # gpio19 tx0 ??
        cs.switch_to_output()
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)  # gpio14, gpio15, gpio8 sck1 tx1 rx1
        self.mcp = None
        try:
            self.mcp = CAN(spi, cs, baudrate=1000000)
        except:
            print("CAN BUS CANNOT BE MADE")


can_bus = CANBus()

while True:
    cm = CanMessage(DEVICE)
    if cm.encode_data(1, number=7):
        print("can msg build worked")
    else:
        print("encode data failed")
    can_bus.mcp.send(cm.msg)
    break
print("msg sent")