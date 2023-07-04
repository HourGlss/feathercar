import math

import pulseio
import board
import neopixel
import time

min_val = 2000
max_val = -1
steering = pulseio.PulseIn(board.D24)
calibrated = [False, False]
final_cal = False
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = .25
pixel.fill((255, 0, 0))
current_value = None
last_change = None

def normalize_value(value):
    left = (100 + 100)
    top = value - min_val
    bottom = max_val - min_val
    try:
        data = top / bottom
    except ZeroDivisionError:
        bottom = .001
        data = top / bottom

    data *= left
    data = data - 100
    if data > 100:
        return 100
    if data < -100:
        return -100
    return round(data)


while True:
    # Wait for an active pulse
    while len(steering) == 0:
        pass
    # Pause while we do something with the pulses
    steering.pause()

    # Print the pulses. pulses[0] is an active pulse unless the length
    # reached max length and idle pulses are recorded.
    data = None
    try:
        data = steering[0]
    except:
        pass
    if data is not None:
        if data < 14000:
            if data < min_val:
                min_val = data
                if min_val < 770:  # STEERING ONLY
                    calibrated[0] = True
                    # print("bottom")
                    pixel.brightness = .5
            if data > max_val:
                if data < 1850:  # STEERING ONLY
                    if max_val > 1750:  # steering only
                        calibrated[1] = True
                        # print("top")
                        pixel.brightness = .5
                    max_val = data
            if not final_cal:
                print(min_val, max_val)
            else:
                data = normalize_value(data)
                scale = math.floor(data / 5)
                data = scale * 5
                current_time_us = round(time.time_ns() * 1000)
                if last_change is None or current_time_us - last_change > 100:
                    current_value = data
                    last_change = current_time_us
                    print(current_value)
    if calibrated[0] and calibrated[1]:
        if not final_cal:
            final_cal = True
            pixel.brightness = 1
            pixel.fill((0, 255, 0))

    # Clear the rest
    steering.clear()

    # Resume with an 80 microsecond active pulse
    steering.resume(80)
