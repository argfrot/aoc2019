import os

from dataclasses import dataclass
from typing import Callable, Any

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input5.txt')
    with open(input_file, 'r') as f:
        for line in f:
            for value in line.split(','):
                yield int(value)


class Instructions(object):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    END = 99


@dataclass
class Instruction:
    opcode: int
    operands: int
    has_result: bool
    execute: Callable[[Any], int]

INSTRUCTION_MAP = {
    Instructions.ADD: Instruction(opcode=Instructions.ADD, operands=2, has_result=True, execute=lambda x,y: x+y),
    Instructions.MULT: Instruction(opcode=Instructions.MULT, operands=2, has_result=True, execute=lambda x,y: x*y),
    Instructions.INPUT: Instruction(opcode=Instructions.INPUT, operands=0, has_result=True, execute=lambda: None),
    Instructions.OUTPUT: Instruction(opcode=Instructions.OUTPUT, operands=1, has_result=False, execute=lambda x: print(x)),
    Instructions.END: Instruction(opcode=Instructions.END, operands=0, has_result=False, execute=lambda: None),
}

class Computer(object):
    def __init__(self, ram, stdin=None):
        self.pc = 0
        self.ram = ram
        self.stdin = stdin

    def decode(self):
        # fetch
        raw_instr = self.ram[self.pc]
        self.pc += 1
        opcode = raw_instr % 100
        raw_instr = raw_instr // 100
        instruction = INSTRUCTION_MAP[opcode]

        # decode
        operands = []
        for _ in range(instruction.operands):
            immediate_mode = raw_instr % 10 == 1
            raw_instr = raw_instr // 10
            value = self.ram[self.pc]
            self.pc += 1
            if not immediate_mode:
                value = self.ram[value]
            operands.append(value)

        # execute
        if instruction.opcode == Instructions.INPUT:
            result = next(self.stdin)
        else:
            result = instruction.execute(*operands)

        # store result
        if instruction.has_result:
            target = self.ram[self.pc]
            self.pc += 1
            self.ram[target] = result

        return instruction

    def run(self):
        while self.decode().opcode != Instructions.END:
            pass

def part1():
    ram = list(get_input())
    stdin = iter([1])
    computer = Computer(ram, stdin)
    computer.run()
    return ram[0] # 12428642

if __name__ == '__main__':
    part1()
