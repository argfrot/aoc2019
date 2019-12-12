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
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    END = 99


@dataclass
class Instruction:
    opcode: int
    operands: int = 0
    has_result: bool = False
    is_branch: bool = False
    execute: Callable[[Any], int] = lambda: None

INSTRUCTION_MAP = {
    Instructions.ADD: Instruction(opcode=Instructions.ADD, operands=2, has_result=True, execute=lambda x,y: x+y),
    Instructions.MULT: Instruction(opcode=Instructions.MULT, operands=2, has_result=True, execute=lambda x,y: x*y),
    Instructions.INPUT: Instruction(opcode=Instructions.INPUT, operands=0, has_result=True),
    Instructions.OUTPUT: Instruction(opcode=Instructions.OUTPUT, operands=1, execute=lambda x: x),
    Instructions.JUMP_IF_TRUE: Instruction(
        opcode = Instructions.JUMP_IF_TRUE,
        operands = 2,
        is_branch = True,
        execute = lambda cond, dest: dest if cond else None
    ),
    Instructions.JUMP_IF_FALSE: Instruction(
        opcode = Instructions.JUMP_IF_FALSE,
        operands = 2,
        is_branch = True,
        execute = lambda cond, dest: dest if not cond else None
    ),
    Instructions.LESS_THAN: Instruction(
        opcode = Instructions.LESS_THAN,
        operands = 2,
        has_result = True,
        execute = lambda x,y: 1 if x < y else 0
    ),
    Instructions.EQUALS: Instruction(
        opcode = Instructions.EQUALS,
        operands = 2,
        has_result = True,
        execute = lambda x,y: 1 if x == y else 0
    ),
    Instructions.END: Instruction(opcode=Instructions.END, operands=0, has_result=False, execute=lambda: None),
}

class Computer(object):
    def __init__(self, ram, stdin=None, stdout=None):
        self.pc = 0
        self.ram = ram
        self.stdin = stdin
        self.stdout = stdout

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
        elif instruction.is_branch:
            result = instruction.execute(*operands)
            if result is not None:
                self.pc = result
        else:
            result = instruction.execute(*operands)

        if instruction.opcode == Instructions.OUTPUT:
            self.stdout.append(result)

        # store result
        if instruction.has_result:
            target = self.ram[self.pc]
            self.pc += 1
            self.ram[target] = result

        return instruction

    def run(self):
        while self.decode().opcode != Instructions.END:
            pass

def part1(input):
    ram = list(get_input())
    stdin = iter([input])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    return stdout

if __name__ == '__main__':
    print(part1(1)) # 12428642
    print(part1(5)) # 918655
