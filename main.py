from cpu import Cpu
from bus import Bus
import numpy as np

bus = Bus()
cpu = Cpu(bus)
test_data = np.uint8(1)
test_address = np.uint8(1)
cpu.write(test_data, test_address)