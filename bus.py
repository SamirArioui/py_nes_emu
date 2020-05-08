import numpy as np


class Bus:
    def __init__(self):
        self.ram = np.zeros([64 * 1024, ], dtype=np.uint8)

    def write(self, data: np.uint8, address: np.uint16):
        if 0x0000 <= address <= 0xFFFF:
            self.ram[address] = data

    def read(self, address: np.uint16, read_only: bool = False) -> np.uint8:

        if 0x0000 <= address <= 0xFFFF:
            return self.ram[address]
        return np.uint8(0x00)
