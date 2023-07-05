import math
import pulseio
import board
import time
import busio
from digitalio import DigitalInOut
from adafruit_mcp2515.canio import Message, RemoteTransmissionRequest
from adafruit_mcp2515 import MCP2515 as CAN
from canmessage import CanMessage

cs = DigitalInOut(board.CAN_CS)
cs.switch_to_output()
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

class PwmIn:
    min_val: int
    max_val: int
    current_value: None | int
    last_value: None | int
    pulse_in: pulseio.PulseIn
    name: str

    def __init__(self, name, pin,min_to_use,max_to_use):
        self.current_time_us = time.monotonic_ns()
        self.min_val = min_to_use
        self.max_val = max_to_use
        self.last_value = None
        self.current_value = None
        self.pulse_in = pulseio.PulseIn(pin)
        self.name = name

    def normalize_value(self, value):
        left = (100 + 100)
        top = value - self.min_val
        bottom = self.max_val - self.min_val

        try:
            normed_value = top / bottom
        except ZeroDivisionError:
            bottom = 0.001
            normed_value = top / bottom

        normed_value *= left
        normed_value = normed_value - 100

        if normed_value > 100:
            return 100
        if normed_value < -100:
            return -100

        return round(normed_value)

    def get_pulse_data(self):
        while len(self.pulse_in) == 0:
            pass

        self.pulse_in.pause()

        pulse_data = None
        try:
            pulse_data = self.pulse_in[0]
        except:
            pass

        if pulse_data is not None:
            if pulse_data < 14000:
                self.current_value = self.normalize_value(pulse_data)
                scale = math.floor(self.current_value / 10)
                self.current_value = scale * 10

                if self.name == "steering":
                    # fucking steering
                    failure = False
                    if self.last_value == 0 and self.current_value == 100:
                        self.current_value = 0
                        failure = True

                    if self.last_value == -100 and self.current_value == 100:
                        self.current_value = -100
                        failure = True

                    if not failure:
                        if self.last_value != self.current_value:
                            self.last_value = self.current_value
                else:

                    if self.last_value != self.current_value:
                        self.last_value = self.current_value

        self.pulse_in.clear()
        self.pulse_in.resume(80)


steering = PwmIn("steering", board.D12,950,1850)
throttle = PwmIn("throttle", board.D25,970,1850)
can_bus = CAN(spi, cs,baudrate=1000000)
cm = CanMessage()
cm.next()
cm.reset()
while True:
    with can_bus.listen() as listener:
        steering.get_pulse_data()
        throttle.get_pulse_data()
        if steering.current_value is not None and throttle.current_value is not None:
            print(f"{steering.current_value:>4}{throttle.current_value:>4}")
