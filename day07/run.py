import os

from dataclasses import dataclass
from typing import Callable, Any

from itertools import permutations

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input7.txt')
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
Instruction(opcode=Instructions.END)


class Computer(object):
    def __init__(self, ram, stdout=None):
        self.pc = 0
        self.ram = ram
        self.stdout = stdout

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
                raw_instr = raw_instr // 10
                value = self.ram[self.pc]
                self.pc += 1
                if not immediate_mode:
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
                try:
                    self.stdout.send(result)
                except StopIteration:
                    pass

            # store result
            if instruction.has_result:
                target = self.ram[self.pc]
                self.pc += 1
                self.ram[target] = result
            
            if instruction.opcode == Instructions.END:
                break

def receive():
    l = []
    while True:
        result = yield l
        l.append(result)

def pipe(destination):
    while True:
        result = yield
        try:
            destination.send(result)
        except StopIteration:
            pass

def dest_pipe():
    # first thing this pipe gets is it's destination
    destination = yield
    phase = yield
    destination.send(None)
    destination.send(phase)
    destination.send(0)
    while True:
        result = yield
        try:
            destination.send(result)
        except StopIteration:
            pass


def amplifier(get_program, stdout):
    ram = list(get_program())
    computer = Computer(ram, stdout).run()
    computer.send(None)
    try:
        while True:
            item = yield
            computer.send(item)
    except StopIteration:
        pass

def calculate_max_thrust(phase_settings, get_program=get_input):
    amps = {}
    stdout = receive()
    stdout.send(None)

    # dp = dest_pipe()
    # dp.send(None)

    amps[4] = amplifier(get_program, stdout)
    p = pipe(amps[4])
    p.send(None)
    amps[3] = amplifier(get_program, p)
    p = pipe(amps[3])
    p.send(None)
    amps[2] = amplifier(get_program, p)
    p = pipe(amps[2])
    p.send(None)
    amps[1] = amplifier(get_program, p)
    p = pipe(amps[1])
    p.send(None)
    amps[0] = amplifier(get_program, p)


    for i, phase in enumerate(phase_settings):
        amps[i].send(None)
        amps[i].send(phase)

    try:
        amps[0].send(0)
        # dp.send(amps[0])
        # dp.send(phase_settings[0])
    except StopIteration:
        pass

    result = stdout.send(None)
    return result[0]

def part1():
    # return calculate_max_thrust([1,2,3,4,5])
    return max(calculate_max_thrust(phase_settings) for phase_settings in permutations(range(5), 5))

if __name__ == '__main__':
    print(part1()) # 46248
