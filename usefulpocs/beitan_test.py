from __future__ import annotations

import board
import busio
import storage
import sdcardio

class GPS:
    zeroes: int
    uart: busio.UART
    data: str

    def __init__(self, uart):
        self.uart = uart
        self.zeroes = 0
        self.data = ''

    def read(self) -> str|None:
        datapart = self.uart.readline()
        str_data = None
        if datapart is not None:
            str_data = datapart.decode('UTF-8').strip()
        if str_data is not None:
            return str_data
        return None



gps = GPS(busio.UART(rx=board.D13, tx=board.D12, baudrate=9600, timeout=0.01))
spi = busio.SPI(board.D6, MOSI=board.SCL, MISO=board.TX)
sdcard = sdcardio.SDCard(spi, board.D5)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
with open("/sd/pico.txt", "w") as file:
    file.write("START LOG")
print("Recording")
while True:
    datapart = gps.read()
    if datapart is not None:
        with open("/sd/pico.txt", "a") as file:
            file.write(f"{datapart}\n")
