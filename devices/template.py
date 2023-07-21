
from enum import Enum


class State(Enum):
    STARTUP = 0
    OPERATE = 1
    SHUTDOWN = 2


class Device:
    device_number: int
    bus: CANBus
    state: State

    def __init__(self, device_number):
        self.device_number = device_number
        self.canbus = CANBus(self.device_number)
        self.state = State.STARTUP
