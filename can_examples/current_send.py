# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
from time import sleep
import board
import busio
from digitalio import DigitalInOut
from adafruit_mcp2515.canio import Message, RemoteTransmissionRequest
from adafruit_mcp2515 import MCP2515 as CAN
from canmessage.canmessage import CanMessage

cs = DigitalInOut(board.CAN_CS)
cs.switch_to_output()
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

can_bus = CAN(spi, cs,baudrate=1000000)
cm = CanMessage()
cm.next()
cm.reset()
while True:
    with can_bus.listen() as listener:
        cm.next()
        message = Message(cm.id, data=cm.data)
        cm.reset()
        send_success = can_bus.send(message)
        print("Send success:", send_success)
        print(f"Send details: id{message.id} d{message.data}")
        message_count = listener.in_waiting()
        print(message_count, "messages available")
        for _i in range(message_count):
            msg = listener.receive()
            print("Message from ", hex(msg.id))
            if isinstance(msg, Message):
                print("message data:", msg.data)
            if isinstance(msg, RemoteTransmissionRequest):
                print("RTR length:", msg.length)
    sleep(1)