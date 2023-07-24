import board
import busio
import digitalio
import os

# For most CircuitPython boards:
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)


class Mitm:
    name: str
    zeroes: int
    uart: busio.UART
    data: bytes

    def __init__(self, uart, name):
        self.name = name
        self.uart = uart
        self.zeroes = 0
        self.data = b''

    def read_and_forward(self) -> None:
        datapart = self.uart.read()
        if datapart is None:
            self.zeroes += 1
            if self.zeroes > 10:
                if self.data != b'':
                    self.print_data()
                    self.data = b''
                    self.zeroes = 0
        elif datapart is not None:
            self.uart.write(datapart)
            self.data += datapart

    def print_data(self) -> None:
        """Log and output a byte array in a readable way."""
        bs = ["%02x".upper() % b for b in self.data]
        print(self.name," ".join(bs))


from_lidar = Mitm(busio.UART(
    tx=board.GP4,
    rx=board.GP5,
    baudrate=115200,
    bits=8,
    parity=busio.UART.Parity.ODD,
    stop=1,
    timeout=.001), "from lidar")
from_usb = Mitm(busio.UART(
    tx=board.GP12,
    rx=board.GP13,
    baudrate=115200,
    bits=8,
    parity=busio.UART.Parity.ODD,
    stop=1,
    timeout=.001), "from usb  ")
print("STARTING")
while True:
    from_usb.read_and_forward()
    from_lidar.read_and_forward()
