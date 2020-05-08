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

        # variables
        self.fetched = np.uint8(0x00)
        self.abs_address = np.uint16(0x0000)
        self.rel_address = np.uint8(0x00)
        self.ops_code = np.uint8(0x00)
        self.cycle = 0

    def write(self, data: np.uint8, address: np.uint16):
        self.bus.write(data, address)

    def read(self, address: np.uint16, read_only: bool = False):
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
    def IMP(self) -> int:
        self.fetched = self.accumulator
        return 0

    def IMM(self) -> int:
        self.abs_address = self.prg_counter + np.uint16(1)
        return 0

    def ZPO(self) -> int:
        self.abs_address = np.uint16(self.read(self.prg_counter))
        self.prg_counter = self.prg_counter + np.uint16(1)
        self.abs_address &= np.uint16(0x00FF)
        return 0

    def ZPX(self) -> int:
        self.abs_address = self.read(self.prg_counter) + self.x_register
        self.prg_counter = self.prg_counter + np.uint16(1)
        self.abs_address &= np.uint16(0x00FF)
        return 0

    def ZPY(self) -> int:
        self.abs_address = self.read(self.prg_counter) + self.y_register
        self.prg_counter = self.prg_counter + np.uint16(1)
        self.abs_address &= np.uint16(0x00FF)
        return 0

    def ABS(self) -> int:
        lo = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        hi = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        self.abs_address = (hi << 8) | lo
        return 0

    def ABX(self) -> int:
        lo = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        hi = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        self.abs_address = (hi << 8) | lo
        self.abs_address += self.x_register

        if self.abs_address & np.uint16(0x00FF) != (hi << 8):
            return 1
        else:
            return 0

    def ABY(self) -> int:
        lo = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        hi = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        self.abs_address = (hi << 8) | lo
        self.abs_address += self.y_register

        if self.abs_address & np.uint16(0x00FF) != (hi << 8):
            return 1
        else:
            return 0

    def IND(self) -> int:
        lo = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        hi = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        pointer = (hi << 8) | lo

        if lo == 0x00FF:
            self.abs_address = (self.read(pointer & np.uint16(0xFF00)) << 8) | self.read(pointer + np.uint16(0))
        else:
            self.abs_address = (self.read(pointer + np.uint16(1)) << 8) | self.read(pointer + np.uint16(0))
        return 0

    def IZX(self) -> int:
        t = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        lo_pointer = np.uint16((t + self.x_register)) & np.uint16(0x00FF)
        hi_pointer = (lo_pointer + np.uint16(1)) & np.uint16(0x00FF)

        lo = self.read(lo_pointer)
        hi = self.read(hi_pointer)
        self.abs_address = (hi << 8) | lo
        return 0

    def IZY(self) -> np.uint8:
        t = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)

        lo = np.uint16(self.read(t & np.uint16(0x00FF)))
        hi = np.uint16(self.read(t + np.uint16(1) & np.uint16(0x00FF)))
        self.abs_address = (hi << 8) | lo
        self.abs_address += self.y_register

        if (self.abs_address & 0xFF00) != (hi << 8):
            return 1
        else:
            return 0

    def REL(self) -> int:
        self.rel_address = self.read(self.prg_counter)
        self.prg_counter = self.prg_counter + np.uint16(1)
        if self.rel_address & 0x80:
            self.rel_address |= 0xFF00
        return 0

    # opcodes
    def ADC(self) -> np.uint8:
        pass

    def AND(self) -> np.uint8:
        pass

    def ASL(self) -> np.uint8:
        pass

    def BCC(self) -> np.uint8:
        pass

    def BCS(self) -> np.uint8:
        pass

    def BEQ(self) -> np.uint8:
        pass

    def BIT(self) -> np.uint8:
        pass

    def BMI(self) -> np.uint8:
        pass

    def BNE(self) -> np.uint8:
        pass

    def BPL(self) -> np.uint8:
        pass

    def BRK(self) -> np.uint8:
        pass

    def BVC(self) -> np.uint8:
        pass

    def BVS(self) -> np.uint8:
        pass

    def CLC(self) -> np.uint8:
        pass

    def CLD(self) -> np.uint8:
        pass

    def CLI(self) -> np.uint8:
        pass

    def CLV(self) -> np.uint8:
        pass

    def CMP(self) -> np.uint8:
        pass

    def CPX(self) -> np.uint8:
        pass

    def CPY(self) -> np.uint8:
        pass

    def DEC(self) -> np.uint8:
        pass

    def DEX(self) -> np.uint8:
        pass

    def DEY(self) -> np.uint8:
        pass

    def EOR(self) -> np.uint8:
        pass

    def INC(self) -> np.uint8:
        pass

    def INX(self) -> np.uint8:
        pass

    def INY(self) -> np.uint8:
        pass

    def JMP(self) -> np.uint8:
        pass

    def JSR(self) -> np.uint8:
        pass

    def LDA(self) -> np.uint8:
        pass

    def LDX(self) -> np.uint8:
        pass

    def LDY(self) -> np.uint8:
        pass

    def LSR(self) -> np.uint8:
        pass

    def CMP(self) -> np.uint8:
        pass

    def NOP(self) -> np.uint8:
        pass

    def ORA(self) -> np.uint8:
        pass

    def PHA(self) -> np.uint8:
        pass

    def PHP(self) -> np.uint8:
        pass

    def PLA(self) -> np.uint8:
        pass

    def PLP(self) -> np.uint8:
        pass

    def ROL(self) -> np.uint8:
        pass

    def ROR(self) -> np.uint8:
        pass

    def RTI(self) -> np.uint8:
        pass

    def RTS(self) -> np.uint8:
        pass

    def SBC(self) -> np.uint8:
        pass

    def SEC(self) -> np.uint8:
        pass

    def SED(self) -> np.uint8:
        pass

    def SEI(self) -> np.uint8:
        pass

    def STA(self) -> np.uint8:
        pass

    def STX(self) -> np.uint8:
        pass

    def STY(self) -> np.uint8:
        pass

    def TAX(self) -> np.uint8:
        pass

    def TAY(self) -> np.uint8:
        pass

    def TSX(self) -> np.uint8:
        pass

    def TXA(self) -> np.uint8:
        pass

    def TXS(self) -> np.uint8:
        pass

    def TYA(self) -> np.uint8:
        pass

    def CMP(self) -> np.uint8:
        pass

    # other function of the cpu
    def clock(self):
        # TODO implement cycle function
        pass

    def reset(self):
        pass

    def irq(self):
        pass

    def nmi(self):
        pass

    # helper function
    def fetch(self) -> np.uint8:
        pass














