from copy import deepcopy
"""
This file generates the hex file for the Control Unit ROM

ROM has 9 lines for address and 16 for data

ROM address layout:
A0-A3: microcode counter
A4-A6: instruction decoder
A7: zero bit
A8: carry bit
"""

"""
Microcode definitions
"""
HLT = 0b1000000000000000    # Halt
MI = 0b0100000000000000     # Memory Address Register In
RI = 0b0010000000000000     # RAM In
RO = 0b0001000000000000     # RAM Out
IO = 0b0000100000000000     # Instruction Register Out
II = 0b0000010000000000     # Instruction Register In
AI = 0b0000001000000000     # Register A in
AO = 0b0000000100000000     # Register A out
EO = 0b0000000010000000     # Sum register out
SU = 0b0000000001000000     # Subtract
BI = 0b0000000000100000     # Register B in
OI = 0b0000000000010000     # Output register in
CE = 0b0000000000001000     # Counter Enable
CO = 0b0000000000000100     # Counter out
J = 0b0000000000000010      # Jump


FETCH = [CO|MI, RO|II|CE]
"""
ROM content
"""
base_data = [
    [*FETCH, 0, 0, 0, 0, 0, 0],                 # 0000 - NOP
    [*FETCH, IO|MI, RO|AI, 0, 0, 0, 0],         # 0001 - LDA
    [*FETCH, IO|MI, RO|BI, EO|AI, 0, 0, 0],     # 0010 - ADD
    [*FETCH, IO|MI, RO|BI, EO|AI|SU, 0, 0, 0],  # 0011 - SUB
    [*FETCH, IO|MI, AO|RI, 0, 0, 0, 0],         # 0100 - STA
    [*FETCH, IO|AI, 0, 0, 0, 0, 0],             # 0101 - LDI
    [*FETCH, IO|J, 0, 0, 0, 0, 0],              # 0110 - JMP
    [*FETCH, 0, 0, 0, 0, 0, 0],                 # 0111 - JZ
    [*FETCH, 0, 0, 0, 0, 0, 0],                 # 1000 - JC
    [*FETCH, 0, 0, 0, 0, 0, 0],                 # 1001
    [*FETCH, 0, 0, 0, 0, 0, 0],                 # 1010
    [*FETCH, 0, 0, 0, 0, 0, 0],                 # 1011
    [*FETCH, 0, 0, 0, 0, 0, 0],                 # 1100
    [*FETCH, 0, 0, 0, 0, 0, 0],                 # 1101
    [*FETCH, AO|OI, 0, 0, 0, 0, 0],             # 1110 - OUT
    [*FETCH, HLT, 0, 0, 0, 0, 0],               # 1111 - HLT
]

data = []

for i in range(0, 4):
    zero_bit = (i&0b10)>>1
    carry_bit = i&0b1
    template = deepcopy(base_data)
    if zero_bit == 1:    # zero bit is set
        template[7][2] = IO|J
    if carry_bit == 1:   # carry bit is set
        template[8][2] = IO|J
    data += template


"""
Write to file
"""
file = open("../bin/ROM", "w")
file.write("v2.0 raw\n")


def formatter(item):
    return str(hex(item))[2:]


for instruction in data:
    for word in instruction:
        nibbles = ''.join(map(formatter, [(word & 0xf000) >> 12,
                                          (word & 0xf00) >> 8,
                                          (word & 0xf0) >> 4,
                                          (word & 0xf)]))
        file.write(nibbles + " ")

file.close()
