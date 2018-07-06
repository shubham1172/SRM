"""
Assembler for the CPU

Generates a hex file from an assembly file

There are two formats of instructions:

type1:
    MNEMONIC OPERAND
type2:
    MNEMONIC
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='file to be assembled')
file_name = parser.parse_args().file

"""
Instruction definitions
"""
type_1 = {"LDA": "1",
          "ADD": "2",
          "SUB": "3",
          "STA": "4",
          "LDI": "5",
          "JMP": "6",
          }

type_2 = {"NOP": "0",
          "OUT": "e",
          "HLT": "f",
          }

"""
Parse the file
"""


class Error(Exception):
    pass


class AssemblerError(Error):
    """
    Exception raised for errors in the syntax
    """

    def __init__(self, lnum, message):
        self.lnum = lnum
        self.message = message + " line: " + str(lnum)

    def __str__(self):
        return self.message


def formatter(item):
    def custom(foo):
        return str(hex(foo))[2:]

    item = int(item)
    nibbles = [(item & 0xf00) >> 8,
               (item & 0xf0) >> 4,
               (item & 0xf)]
    return ''.join(map(custom, nibbles))


line_number = 0
file = open(file_name, 'r')
lines = file.read().strip().split('\n')
file.close()

data = "v2.0 raw\n"

for line in lines:
    line = line.split(';')[0].strip()
    if line == "":
        continue
    tokens = line.split(' ')
    if len(tokens) == 0:
        continue
    elif len(tokens) == 1:
        if tokens[0].upper() not in type_2.keys():
            raise AssemblerError(line_number, "Invalid syntax")
        data += (type_2[tokens[0].upper()] + "000 ")
    elif len(tokens) == 2:
        if tokens[0].upper() not in type_1.keys():
            raise AssemblerError(line_number, "Invalid syntax")
        if not tokens[1].isdigit() or int(tokens[1]) >= (2 ** 12):
            raise AssemblerError(line_number, "Invalid syntax")
        data += (type_1[tokens[0].upper()] + formatter(tokens[1]) + " ")
    else:
        raise AssemblerError(line_number, "Invalid syntax")
    line_number += 1

file = open(file_name.split('/')[-1] + ".bin", 'w+')
file.write(data)
file.close()
