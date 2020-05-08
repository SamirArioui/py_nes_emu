from bus import Bus
import numpy as np


class Cpu:
    def __init__(self, bus: Bus):
        # connect bus
        self.bus = bus

        # flags of status register
        self.status_flags = {
            "carry": (np.uint8(1) << np.uint8(0)),
            "zero": (np.uint8(1) << np.uint8(1)),
            "interrupts": (np.uint8(1) << np.uint8(2)),
            "decimal": (np.uint8(1) << np.uint8(3)),
            "break": (np.uint8(1) << np.uint8(4)),
            "unused": (np.uint8(1) << np.uint8(5)),
            "overflow": (np.uint8(1) << np.uint8(6)),
            "negative": (np.uint8(1) << np.uint8(7))
        }

        # status register
        self.status_register = np.uint8(0x00)

        # accumulator and x, y index register
        self.x_register = np.uint8(0x00)
        self.y_register = np.uint8(0x00)
        self.accumulator = np.uint8(0x00)

        # programme counter and stack pointer
        self.prg_counter = np.uint16(0x0000)
        self.stack_pointer = np.uint8(0x00)

    def write(self, data: np.uint8, address: np.uint16):
        self.bus.write(data, address)

    def read(self, address: np.uint16, read_only: bool = False) -> np.uint8:
        return self.bus.read(address)

    def set_flag(self, flag_status: str, state: bool):
        # TODO check if valid flag_status
        if state:
            self.status_register |= self.status_flags[flag_status]
        else:
            self.status_register &= ~self.status_flags[flag_status]

    def get_flag(self, flag_status: str) -> np.uint8:
        # TODO check if valid flag_status
        flag_state = self.status_register & self.status_flags[flag_status]
        return np.uint8(flag_state)

    # addressing modes
    def imp(self) -> np.uint8:
        """
        implied addressing mode:
        the address containing the operand is implicitly stated in the
        operation code of the instruction
        """
        pass

    def imm(self) -> np.uint8:
        """
        immediate addressing mode:
        the second byte of the instruction contains the operand
        """
        pass

    def zp0(self) -> np.uint8:
        """
        zero page addressing mode:
        fetch only the second byte of the instruction and assuming
        a zero high address byte
        """
        pass

    def zpx(self) -> np.uint8:
        """
        zero page addressing mode with x:
        same as the zero page addressing mode but we add x register content to
        the second byte of the instruction
        val = PEEK((arg + X) % 256)
        """
        pass

    def zpy(self) -> np.uint8:
        """
        zero page addressing mode with y:
        same as the zero page addressing mode but we add y register content to
        the second byte of the instruction
        val = PEEK((arg + Y) % 256)
        """
        pass

    def abs(self) -> np.uint8:
        """
        absolute addressing mode:
        the second byte of the instruction is the 8 low order bits of the
        address
        the third byte of the instruction is the 8 high order bits of the
        address
        """
        pass

    def abx(self) -> np.uint8:
        """
        absolute addressing mode with x:
        same as th absolute addressing mode but we add x register content to
        the second and third bytes of th instruction
        val = PEEK(arg + X)
        """
        pass

    def aby(self) -> np.uint8:
        """
        absolute addressing mode with y:
        same as th absolute addressing mode but we add x register content to
        the second and third bytes of th instruction
        val = PEEK(arg + Y)
        """
        pass

    def ind(self) -> np.uint8:
        """
        indirect addressing mode:
        """
        pass

    def izx(self) -> np.uint8:
        """
        indexed indirect addressing mode:
        the second byte of the instruction is added to the content of
        x register discarding the carry. the result point to a memory location
        on page zero which contains the low order byte of the effective address
        the next memory location contains the high order byte of the effective
        address.
        val = PEEK(PEEK((arg + X) % 256) + PEEK((arg + X + 1) % 256) * 256
        """
        pass

    def izy(self) -> np.uint8:
        """
        indirect indexed addressing mode:
        the second byte of the instruction point to a memory location in
        page zero. The contents of this memory location are added to the
        contents of y register. The result is the low order byte of effective
        address. The carry of this addition is added to the content of the next
        page zero memory location, to form the high order byte of the effective
        address
        val = PEEK(PEEK(arg) + PEEK((arg + 1) % 256) * 256 + Y)
        """
        pass

    def rel(self) -> np.uint8:
        """
        relative addressing mode:
        the second byte of the instruction is an operand. This operand
        is an offset which is added to the program counter when the counter
        is set at the next instruction
        """
        pass

    # opcodes






