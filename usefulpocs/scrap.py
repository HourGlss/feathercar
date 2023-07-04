import pulseio
import board
import math

min_val = 2000
max_val = -1
received_values = 0
steering = pulseio.PulseIn(board.D24)
calibrated = False


def normalize_value(value):
    left = (100 + 100)
    top = value - min_val
    bottom = max_val - min_val
    data = top/bottom
    data *= left
    data = data - 100
    if data > 100:
        return 100
    if data < -100:
        return -100
    return round(data)


print("keep stick neutral")
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
        if data < 10000:
            received_values += 1
            if not calibrated:
                if data < min_val:
                    min_val = data
                if data > max_val:
                    max_val = data
                if received_values == 200:
                    print("ALL LEFT")
                if received_values == 400:
                    print("ALL RIGHT")
    except:
        pass
    if received_values > 600:
        calibrated = True
    if calibrated:
        print(normalize_value(data))

    # Clear the rest
    steering.clear()

    # Resume with an 80 microsecond active pulse
    steering.resume(80)
