import os

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Any

from itertools import permutations

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input9.txt')
    with open(input_file, 'r') as f:
        for line in f:
            for value in line.split(','):
                yield int(value)

def coroutine(f):
    def start(*args,**kwargs):
        try:
            coro = f(*args,**kwargs)
            coro.send(None)
        except StopIteration:
            pass
        return coro
    return start


class Instructions(object):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9
    END = 99


@dataclass
class Instruction:
    opcode: int
    operands: int = 0
    has_result: bool = False
    is_branch: bool = False
    execute: Callable[[Any], int] = lambda: None

    def __post_init__(self):
        if not 'lookup' in Instruction.__dict__:
            Instruction.lookup = {}
        Instruction.lookup[self.opcode] = self

Instruction(opcode=Instructions.ADD, operands=2, has_result=True, execute=lambda x,y: x+y)
Instruction(opcode=Instructions.MULT, operands=2, has_result=True, execute=lambda x,y: x*y)
Instruction(opcode=Instructions.INPUT, has_result=True)
Instruction(opcode=Instructions.OUTPUT, operands=1, execute=lambda x: x)
Instruction(
    opcode = Instructions.JUMP_IF_TRUE,
    operands = 2,
    is_branch = True,
    execute = lambda cond, dest: dest if cond else None
)
Instruction(
    opcode = Instructions.JUMP_IF_FALSE,
    operands = 2,
    is_branch = True,
    execute = lambda cond, dest: dest if not cond else None
)
Instruction(
    opcode = Instructions.LESS_THAN,
    operands = 2,
    has_result = True,
    execute = lambda x,y: 1 if x < y else 0
)
Instruction(
    opcode = Instructions.EQUALS,
    operands = 2,
    has_result = True,
    execute = lambda x,y: 1 if x == y else 0
)
Instruction(opcode=Instructions.ADJUST_RELATIVE_BASE, operands=1, execute=lambda x: x)
Instruction(opcode=Instructions.END)

class Computer(object):
    def __init__(self, ram, stdout=None):
        self.pc = 0
        self.relative_base = 0
        self.ram = ram
        self.stdout = stdout

    @coroutine
    def run(self):
        while True:
            # fetch
            raw_instr = self.ram[self.pc]
            self.pc += 1
            opcode = raw_instr % 100
            raw_instr = raw_instr // 100
            instruction = Instruction.lookup[opcode]

            # decode
            operands = []
            for _ in range(instruction.operands):
                immediate_mode = raw_instr % 10 == 1
                relative_mode = raw_instr % 10 == 2
                raw_instr = raw_instr // 10
                value = self.ram[self.pc]
                self.pc += 1
                if relative_mode:
                    value = self.ram[self.relative_base + value]
                elif not immediate_mode:
                    value = self.ram[value]
                operands.append(value)

            # execute
            if instruction.opcode == Instructions.INPUT:
                result = yield
            elif instruction.is_branch:
                result = instruction.execute(*operands)
                if result is not None:
                    self.pc = result
            else:
                result = instruction.execute(*operands)

            if instruction.opcode == Instructions.OUTPUT:
                self.stdout.send(result)
            elif instruction.opcode == Instructions.ADJUST_RELATIVE_BASE:
                self.relative_base += result

            # store result
            if instruction.has_result:
                target = self.ram[self.pc]
                self.pc += 1
                relative_mode = raw_instr % 10 == 2
                if relative_mode:
                    target = target + self.relative_base
                self.ram[target] = result
            
            if instruction.opcode == Instructions.END:
                break

@coroutine
def receive(output):
    while True:
        result = yield
        output.append(result)

@coroutine
def pipe(destination):
    while True:
        result = yield
        try:
            destination.send(result)
        except StopIteration:
            pass

def infinite_ram(ram):
    return defaultdict(int, {i: v for i, v in enumerate(ram)})

@coroutine
def execute(get_program, stdout):
    ram = infinite_ram(get_program())
    computer = Computer(ram, stdout).run()
    try:
        while True:
            item = yield
            computer.send(item)
    except StopIteration:
        pass

def run_computer(input, get_program=get_input):
    stdout = []
    out = receive(stdout)

    computer = execute(get_program, out)
    try:
        computer.send(input)
    except StopIteration:
        pass

    return stdout

def part1():
    return run_computer(1)

def part2():
    return run_computer(2)


if __name__ == '__main__':
    print(part1()) # 3454977209
    print(part2()) # 50120
