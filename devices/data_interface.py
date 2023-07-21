from __future__ import annotations

import socket
from can_info.canbus import CANBus
from enum import Enum

try:
    from canmessage import CanMessage
except:
    try:
        from can_info.canmessage import CanMessage
    except:
        print("Can lib not found")


class ConnectionType(Enum):
    CAN = 0
    SOCKET = 1


class Bus:
    connection_type: ConnectionType
    device_number: int
    connection: socket.socket | CANBus

    next_message_to_send: CanMessage | None
    received_messages: list

    socket_port_to_send_to: str | None
    socket_port_listen_on: str | None

    def __init__(self, device, type_of_connection: ConnectionType, port_to_send_to: str = None,
                 port_to_listen_on: str = None):
        self.device_number = device
        self.connection_type = type_of_connection

        self.received_messages = []
        self.create_bus_connection()
        self.socket_port_listen_on = None
        self.socket_port_to_send_to = None

        if self.connection_type == ConnectionType.SOCKET:
            assert port_to_listen_on is not None
            assert port_to_send_to is not None
            self.socket_port_listen_on = port_to_listen_on
            self.socket_port_to_send_to = port_to_send_to

    def create_bus_connection(self):

        if self.connection_type == ConnectionType.CAN:
            self.connection = CANBus(self.device_number)
        elif self.connection_type == ConnectionType.SOCKET:
            self.connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.connection.bind(("0.0.0.0",self.socket_port_listen_on))
            self.connection.setblocking(True)
            self.connection.settimeout(.001)

    def create_message(self):
        pass

    def send(self):
        pass

    def listen(self):
        if self.connection_type == ConnectionType.CAN:
            self.connection.listen()
        elif self.connection_type == ConnectionType.SOCKET:
            message,address = self.connection.recvfrom(1024)



if __name__ == "__main__":
    b = Bus(1, ConnectionType.SOCKET)
