import board
import busio
import time
import math
import adafruit_hcsr04
in_front_distance = None
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP16, echo_pin=board.GP17)
def send_break_signal():
    print("BREAK")

while True:
    try:
        in_front_distance = (sonar.distance,)[0]
    except RuntimeError:
        continue
    if in_front_distance is not None:
        if in_front_distance < 30:
            send_break_signal()
    time.sleep(0.1)