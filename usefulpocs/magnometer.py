# # HMC5883L
# # https://cdn-shop.adafruit.com/datasheets/HMC5883L_3-Axis_Digital_Compass_IC.pdf
# # http://magnetic-declination.com
from __future__ import annotations

import board
import busio
import storage
import sdcardio
import time
import math


class HMC5883L:
    gain_config = [1370, 1090, 820, 660, 440, 390, 330, 230]
    dig_res_per_gain = [.73, .92, 1.22, 1.52, 2.27, 2.56, 3.03, 4.35]
    register_info = [
        (0x00, "Configuration Register A", "rw"),
        (0x01, "Configuration Register B", "rw"),
        (0x02, "Mode Register", "rw"),
        (0x03, "Data Output X MSB Register", "r"),
        (0x04, "Data Output X LSB Register", "r"),
        (0x05, "Data Output Z MSB Register", "r"),
        (0x06, "Data Output Z LSB Register", "r"),
        (0x07, "Data Output Y MSB Register", "r"),
        (0x08, "Data Output Y LSB Register", "r"),
        (0x09, "Status Register", "r"),
        (0x10, "Identification Register A", "r"),
        (0x11, "Identification Register B", "r"),
        (0x12, "Identification Register C", "r"),
    ]
    device_address: int
    i2c: busio.I2C
    gain: int 
    declination: float

    def __init__(self, i2c, device_address, gain=None, declination=0.0):
        self.i2c = i2c
        self.device_address = device_address
        if gain is None:
            self.auto_adjust_gain()
        else:
            self.gain = gain
        self.declination = declination

    def _read_register(self, register_address):
        time.sleep(.006)
        data = bytearray(1)
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(self.device_address, bytes([register_address]))
            self.i2c.readfrom_into(self.device_address, data)
        finally:
            self.i2c.unlock()
        return data[0]

    def _read_bcd_register(self, register_address):
        msb = self._read_register(register_address)
        lsb = self._read_register(register_address + 1)
        return (msb << 8) | lsb

    def _write_to_register(self, register_address, data_byte):
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(self.device_address, bytes([register_address, data_byte]))
        finally:
            self.i2c.unlock()
        time.sleep(.0025)

    def _read_all_registers(self):
        register_data = []
        for address, name, access in self.register_info:
            value = self._read_register(address)
            register_data.append(value)
        return register_data

    def _set_continuous_mode(self):
        self._write_to_register(0x02, 0x00)

    def _set_single_measurement_mode(self):
        self._write_to_register(0x02, 0x01)

    def x(self):
        return self._read_bcd_register(0x03)

    def y(self):
        return self._read_bcd_register(0x07)

    def z(self):
        return self._read_bcd_register(0x05)

    def _adjust_gain_lower(self):
        if self.gain > 0:
            self.gain -= 1
            return True
        return False

    def _set_gain(self, chosen_gain) -> bool:
        if 0 <= chosen_gain <= 7:
            self.gain = chosen_gain
            return True
        return False

    def _adjust_gain_higher(self):
        if self.gain < 7:
            self.gain += 1
            return True
        return False

    def _create_gain_register_info(self):
        return self.gain << 5

    def _get_low_high_self_test(self):

        low = 243
        high = 575
        return int(low * (self.gain_config[self.gain] / 390)), int(high * (self.gain_config[self.gain] / 390))

    def _single_self_test(self):
        # Step 1: Write CRA (00) - send 0x3C 0x00 0x71 (8-average, 15 Hz default, positive self-test measurement)
        self._write_to_register(0x00, 0x71)

        # Step 2: Write CRB (01) - send 0x3C 0x01 0xA0 (Gain=5)
        self._write_to_register(0x01, self._create_gain_register_info())

        self._set_continuous_mode()
        time.sleep(0.006)
        # Trash data pull to adjust for gain change "If gain is changed then this data set is using previous gain"
        # we dont want that
        x, y, z = self.x(), self.y(), self.z()
        time.sleep(.067)  # Wait about 67 ms (if 15 Hz rate) or monitor status register or DRDY hardware interrupt pin
        # Step 3: Write Mode (02) - send 0x3C 0x02 0x00 (Continuous-measurement mode)

        # Step 4: Wait 6 ms or monitor status register or DRDY hardware interrupt pin
        # In this implementation, we'll wait for 6 ms using time.sleep() function

        # Convert three 16-bit 2’s complement hex values to decimal values and assign to X, Z, Y, respectively.
        x = self.x()
        if x >= 32768:
            x -= 65536

        z = self.z()
        if z >= 32768:
            z -= 65536

        y = self.y()
        if y >= 32768:
            y -= 65536

        low_limit, high_limit = self._get_low_high_self_test()
        self_test = False
        if low_limit <= x <= high_limit and low_limit <= y <= high_limit and low_limit <= z <= high_limit:
            self_test = True
        # Write CRA (00) - send 0x3C 0x00 0x70 (Exit self-test mode and this procedure)
        self._write_to_register(0x00, 0x70)
        return self_test

    def auto_adjust_gain(self):
        print("Begin Auto Adjust Gain")
        number_of_tests = 100
        self._set_gain(0)
        i = 0
        while i <= 7:
            passes = 0
            test_results = []
            for _ in range(number_of_tests):
                test_result = self._single_self_test()
                test_results.append(test_result)
            for tr in test_results:
                if tr:
                    passes += 1
            if passes == number_of_tests:
                print(f"Gain set to {self.gain}")
                break
            self._adjust_gain_higher()
            i += 1

    def get_compass(self):
        self._set_single_measurement_mode()
        time.sleep(0.067)
        heading = math.atan2(self.y() / self.gain_config[self.gain], self.x() / self.gain_config[self.gain])
        heading += self.declination
        if heading < 0:
            heading += 2 * math.pi
        if heading > 2 * math.pi:
            heading -= 2 * math.pi
        return heading * (180 / math.pi)


def main():
    mag_i2c = busio.I2C(board.D25, board.D24)
    da = 0x1E
    magnetic_declination = -0.24
    mag = HMC5883L(mag_i2c, da, declination=magnetic_declination)
    while True:
        print(mag.get_compass())


def setup_sdcard():
    spi = busio.SPI(board.D6, MOSI=board.SCL, MISO=board.TX)
    sdcard = sdcardio.SDCard(spi, board.D5)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")


if __name__ == "__main__":
    # setup_sdcard()
    main()
