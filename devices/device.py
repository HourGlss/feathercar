import time
import neopixel
import digitalio
import board



class State:
    TURNON = -1
    EMERGENCY = 0
    STANDBY = 1
    OPERATE = 2

def ms_time():
    return round(time.monotonic_ns()/1000000)

class Device:
    state: int
    start_time: float
    color_states = {
        -1:(127,127,127),
        0:(255,0,0),
        1:(255,127,39),
        2:(0,255,0)
    }
    np: neopixel.NeoPixel

    def __init__(self):
        self.start_time = ms_time()
        print(self.start_time)
        self.state = State.TURNON
        on_indicator = digitalio.DigitalInOut(board.LED)
        on_indicator.direction = digitalio.Direction.OUTPUT
        on_indicator.value = True
        self.initalize()
        self.wait()
        self.state = State.STANDBY
        self.run()

    def initalize(self):
        print("initialize")
        self.np = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.np.brightness = 1
        self.np.fill(self.color_states[self.state])
        pass

    def standby(self):
        print(ms_time())
        pass

    def operate(self):
        print("operate")
        pass

    def emergency(self):
        print("emergency")
        pass

    def wait(self):
        print("waiting")
        time.sleep(5)

    def run(self):
        print("run")
        while True:
            self.np.fill(self.color_states[self.state])
            if self.state == State.OPERATE:
                self.operate()
            elif self.state == State.EMERGENCY:
                self.emergency()
            elif self.state == State.STANDBY:
                self.standby()


if __name__ == "__main__":
    d = Device()