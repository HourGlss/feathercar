import struct
from icd import icd


class CanMessage:
    id: int
    data: bytes
    parsed_data: dict[str:int]
    device: int

    def __init__(self, dev):
        self.id = 0x001
        self.data = b''
        self.device = dev

    def encode_data(self, msg_number: int, **kwargs):
        assert 0 <= msg_number <= 255
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
                struct_format = f"B B {icd[self.device]['messages'][msg_number]['struct_string']}"
                # Pack the numbers into a byte string
                packed_data = struct.pack(struct_format, num1, num2, num3, num4)
                self.data = packed_data
                return True
        return False

    def decode_data(self):
        from_device = int(struct.unpack('B', self.data[0:1])[0])
        msg_number = int(struct.unpack('B', self.data[1:2])[0])
        if from_device == 1:
            if msg_number == 1:
                from_device, msg_number, *the_rest = struct.unpack(
                    f"B B {icd[from_device]['messages'][msg_number]['struct_string']}", self.data)
                parsed_data = dict()
                i = 0
                for item in icd[from_device]['messages'][msg_number]['keywords']:
                    parsed_data[item] = the_rest[i]
                    i += 1
                parsed_data['from'] = from_device
                parsed_data['msg_number'] = msg_number
                self.parsed_data = parsed_data
                return True
        return False


if __name__ == "__main__":
    pass
    # from_device = 1
    # msg_number = 1
    # steering = -100
    # throttle = 100
    # cm = CanMessage(from_device)
    # cb = CanMessage(8)
    # cm.encode_data(msg_number, steering=steering, throttle=throttle)
    # cb.data = cm.data
    # cb.decode_data()
