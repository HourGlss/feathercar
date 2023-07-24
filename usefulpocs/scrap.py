class Foo:
    gain: int

    def __init__(self):
        self.gain = 5

    def adjust_gain_lower(self):
        if self.gain > 0:
            self.gain -= 1
            return True
        return False

    def adjust_gain_higher(self):
        if self.gain < 7:
            self.gain += 1
            return True
        return False

    def set_gain(self, chosen_gain) -> bool:
        if 0 <= chosen_gain <= 7:
            self.gain = chosen_gain
            return True
        return False

    def _create_gain_register_info(self):
        return self.gain << 5

    def _get_low_high_self_test(self):
        gain_config = [1370, 1090, 820, 660, 440, 390, 330, 230]
        low = 243
        high = 575
        return int(low * (gain_config[self.gain] / 390)), int(high * (gain_config[self.gain] / 390))


if __name__ == "__main__":
    f = Foo()
    for i in range(0, 8):
        f.set_gain(i)
        l,h = f.get_min_max()
        print(f"{f.gain} {l} {h}")
