import time
import neopixel
import digitalio
import board
import adafruit_mcp2515
import struct
import busio

icd = {
    1: {  # DEVICE MANUAL CON
        "name": "Manual control",
        "description": "Puts information from controller onto bus",
        "messages": {
            1: {  # MSG NUMBER
                "struct_string": "bb",
                "keywords": ["steering", "throttle"],
                "id": 0x010  # CAN BUS ID
            }
        }
    },
    8: {  # DEVICE TESTING
        "name": "test",
        "description": "Puts SOMETHING on the bus",
        "messages": {
            1: {  # MSG NUMBER
                "struct_string": "b",
                "keywords": ["number"],
                "id": 0x710  # CAN BUS ID
            }
        }
    }
}


class CanMessage:
    id: int | None
    data: bytes
    parsed_data: dict[str:int]
    device_number: int
    msg: adafruit_mcp2515.Message | None

    def __init__(self, device_number, msg=None):
        self.id = None
        self.data = b''
        self.device_number = device_number
        self.msg = None
        if msg is not None:
            self.msg = msg

    def encode_data(self, msg_number: int, **kwargs):
        assert 0 <= msg_number <= 255
        assert self.msg is None
        if self.device_number == 1:
            if msg_number == 1:
                assert 'steering' in kwargs.keys()
                assert 'throttle' in kwargs.keys()
                num1 = self.device_number
                num2 = msg_number
                num3 = kwargs['steering']
                assert -100 <= num3 <= 100
                num4 = kwargs['throttle']
                assert -100 <= num4 <= 100

                # Define the struct format string
                specific = icd[self.device_number]['messages'][msg_number]['struct_string']

                struct_format = f"BB{specific}"
                # Pack the numbers into a byte string
                packed_data = struct.pack(struct_format, num1, num2, num3, num4)
                self.data = packed_data
                self.msg = adafruit_mcp2515.Message(icd[self.device_number]['messages'][msg_number]['id'], self.data)
                return True
        if self.device_number == 8:
            if msg_number == 1:
                assert 'number' in kwargs.keys()
                num1 = self.device_number
                num2 = msg_number
                num3 = kwargs['number']
                assert -128 <= num3 <= 127

                # Define the struct format string
                specific = icd[self.device_number]['messages'][msg_number]['struct_string']

                struct_format = f"BB{specific}"
                # Pack the numbers into a byte string
                packed_data = struct.pack(struct_format, num1, num2, num3)
                self.data = packed_data
                self.msg = adafruit_mcp2515.Message(icd[self.device_number]['messages'][msg_number]['id'], self.data,
                                                    extended=False)
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


class State:
    TURNON = -1
    EMERGENCY = 0
    STANDBY = 1
    OPERATE = 2


def ms_time():
    return round(time.monotonic_ns() / 1000000)


class Device:
    state: int
    start_time: float
    last_heartbeat: float
    received_messages: list
    device_number: int
    matches: tuple
    color_states = {
        -1: (127, 127, 127),
        0: (255, 0, 0),
        1: (255, 127, 39),
        2: (0, 255, 0)
    }
    np: neopixel.NeoPixel
    mcp: adafruit_mcp2515.MCP2515 | None
    next_massage_to_send: CanMessage | None

    def __init__(self, device_number):
        self.next_massage_to_send = None
        self.start_time = ms_time()
        self.last_heartbeat = self.start_time
        self.state = State.TURNON
        on_indicator = digitalio.DigitalInOut(board.LED)
        on_indicator.direction = digitalio.Direction.OUTPUT
        on_indicator.value = True
        self.received_messages = []
        self.initalize()
        self.device_number = device_number
        self.wait()
        self.state = State.STANDBY
        self.run()

    def initalize(self):
        now = ms_time()
        print(f"initialize {now - self.start_time}")
        self.create_bus_connection()
        self.np = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.np.brightness = 1
        self.np.fill(self.color_states[self.state])
        self.matches = (adafruit_mcp2515.Match(0x060, mask=0x7F0, extended=False),)
        pass

    def create_bus_connection(self):
        cs = digitalio.DigitalInOut(board.CAN_CS)
        cs.switch_to_output()
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.mcp = None
        try:
            self.mcp = adafruit_mcp2515.MCP2515(spi, cs, baudrate=1000000)
        except:
            pass
        assert self.mcp is not None

    def standby(self):
        # print(ms_time())
        # if begin_operate in received_messages:
        #    self.state = State.OPERATE
        pass

    def operate(self):
        print("operate")
        try:
            # Perform sensing and populate to_send_on_can buffer
            pass
        except:
            self.state = State.EMERGENCY


        pass

    def emergency(self):
        print("emergency")
        # Try to recover from emergency
        try:
            pass
            #data is valid
            self.state = State.OPERATE
        except:
            pass
        pass

    def wait(self):
        print("waiting")
        time.sleep(5)
        # main controller should not sleep

    def run(self):
        print("run")
        while True:
            now = ms_time()
            with self.mcp.listen(matches=self.matches, timeout=.00001) as listener:
                next_message = listener.receive()
                while next_message is not None:
                    self.received_messages.append(next_message)
                    print("adding message")
                    next_message = listener.receive()
            # Set the neopixel according to device state
            self.np.fill(self.color_states[self.state])

            if now - self.last_heartbeat > 1000:
                self.send_heartbeat()
                self.last_heartbeat = now
            if self.state == State.OPERATE:
                self.operate()
            elif self.state == State.EMERGENCY:
                self.emergency()
            elif self.state == State.STANDBY:
                self.standby()
            if self.next_massage_to_send is not None:
                self.send()

    def create_message(self, message_number, **kwargs):
        cm = CanMessage(self.device_number)
        cm.encode_data(message_number, **kwargs)

    def send(self) -> bool:
        if self.next_massage_to_send is not None:
            self.mcp.send(self.next_massage_to_send.msg)
            self.next_massage_to_send = None
            return True
        return False

    def send_heartbeat(self):
        print("HEARTBEAT OUT")


if __name__ == "__main__":
    d = Device(6)
