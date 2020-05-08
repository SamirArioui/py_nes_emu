from bus import Bus
import numpy as np


class Cpu:
    def __init__(self, bus: Bus):
        # connect bus
        self.bus = bus

        # different flags of status register
        self.status_flags = {
            "carry": (np.uint(1) << np.uint(0)),
            "zero": (np.uint(1) << np.uint(1)),
            "interrupts": (np.uint(1) << np.uint(2)),
            "decimal": (np.uint(1) << np.uint(3)),
            "break": (np.uint(1) << np.uint(4)),
            "unused": (np.uint(1) << np.uint(5)),
            "overflow": (np.uint(1) << np.uint(6)),
            "negative": (np.uint(1) << np.uint(7))
        }

        # status register
        self.status_register = np.uint8(0x00)

        # accumulator and x, y index register
        self.x_register = np.uint8(0x00)
        self.y_register = np.uint8(0x00)
        self.accumulator = np.uint8(0x00)

        # programme counter ans stack pointer
        self.prg_counter = np.uint16(0x0000)
        self.stack_pointer = np.uint8(0x00)

    def write(self, data: np.uint8, address: np.uint16):
        self.bus.write(data, address)

    def read(self, address: np.uint16, read_only: bool = False) -> np.uint8:
        return self.bus.read(address)

    def set_flag(self, flag_status: str, state: bool):
        if state:
            self.status_register |= self.status_flags[flag_status]
        else:
            self.status_register &= ~self.status_flags[flag_status]

    def get_flag(self, flag_status: str) -> np.uint8:
        flag_state = self.status_register & self.status_flags[flag_status]
        return flag_state





