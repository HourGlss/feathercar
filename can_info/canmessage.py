from __future__ import annotations

import struct
from icd import icd
from adafruit_mcp2515.canio import Message, RemoteTransmissionRequest


class CanMessage:
    id: int | None
    data: bytes
    parsed_data: dict[str:int]
    device: int
    msg: Message | None

    def __init__(self, dev, msg=None):
        self.id = None
        self.data = b''
        self.device = dev
        self.msg = None
        if msg is not None:
            self.msg = msg

    def encode_data(self, msg_number: int, **kwargs):
        assert 0 <= msg_number <= 255
        assert self.msg is None
        if self.device == 1:
            if msg_number == 1:
                assert 'steering' in kwargs.keys()
                assert 'throttle' in kwargs.keys()
                num1 = self.device
                num2 = msg_number
                num3 = kwargs['steering']
                assert -100 <= num3 <= 100
                num4 = kwargs['throttle']
                assert -100 <= num4 <= 100

                # Define the struct format string
                specific = icd[self.device]['messages'][msg_number]['struct_string']

                struct_format = f"BB{specific}"
                # Pack the numbers into a byte string
                packed_data = struct.pack(struct_format, num1, num2, num3, num4)
                self.data = packed_data
                self.msg = Message(icd[self.device]['messages'][msg_number]['id'], self.data)
                return True
        if self.device == 8:
            if msg_number == 1:
                assert 'number' in kwargs.keys()
                num1 = self.device
                num2 = msg_number
                num3 = kwargs['number']
                assert -128 <= num3 <= 127


                # Define the struct format string
                specific = icd[self.device]['messages'][msg_number]['struct_string']

                struct_format = f"BB{specific}"
                # Pack the numbers into a byte string
                packed_data = struct.pack(struct_format, num1, num2, num3)
                self.data = packed_data
                self.msg = Message(icd[self.device]['messages'][msg_number]['id'], self.data,extended=False)
                return True
        return False

    def decode_data(self):
        assert self.msg is not None
        self.data = self.msg.data
        self.id = self.msg.id
        from_device = int(struct.unpack('B', self.data[0:1])[0])
        msg_number = int(struct.unpack('B', self.data[1:2])[0])
        if from_device == 1:
            if msg_number == 1:
                if icd[from_device]['messages'][msg_number]['id'] == self.id:
                    from_device, msg_number, *the_rest = struct.unpack(
                        f"BB{icd[from_device]['messages'][msg_number]['struct_string']}", self.data)
                    parsed_data = dict()
                    i = 0
                    for item in icd[from_device]['messages'][msg_number]['keywords']:
                        parsed_data[item] = the_rest[i]
                        i += 1
                    # parsed_data['from'] = from_device
                    # parsed_data['msg_number'] = msg_number
                    self.parsed_data = parsed_data
                    return True
        return False


if __name__ == "__main__":
    pass
    _from_device = 1
    _msg_number = 1
    _steering = 0
    _throttle = 0
    ca = CanMessage(_from_device)
    ca.encode_data(_msg_number, steering=_steering, throttle=_throttle)

    # _to_device = 2
    #
    # cb = CanMessage(_to_device, ca.msg)
    # for k,v in cb.parsed_data.items():
    #     print(k,v)
