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
                self.stdout.send(result)

            # store result
            if instruction.has_result:
                target = self.ram[self.pc]
                self.pc += 1
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

@coroutine
def amplifier(get_program, stdout):
    ram = list(get_program())
    computer = Computer(ram, stdout).run()
    try:
        while True:
            item = yield
            computer.send(item)
    except StopIteration:
        pass

def calculate_max_thrust(phase_settings, get_program=get_input):
    amps = {}
    stdout = [0] # 0 is the initial input to amps[0]
    out = receive(stdout)

    amps[4] = amplifier(get_program, out)
    amps[3] = amplifier(get_program, pipe(amps[4]))
    amps[2] = amplifier(get_program, pipe(amps[3]))
    amps[1] = amplifier(get_program, pipe(amps[2]))
    amps[0] = amplifier(get_program, pipe(amps[1]))

    for i, phase in enumerate(phase_settings):
        amps[i].send(phase)

    # Hooking the coroutines up directly from amps[4] back to amps[0]
    # caused problems as the generators were already executing when it
    # tried to send the output value back to the beginning of the pipeline.
    #
    # This solution explicitly takes the output value and sends it back to
    # the start until the generators exit; each chain of sends unwinds
    # back to here, so it can push the next value in.
    #
    # This was fun getting to know python generators/coroutines a litte
    # more intimately...but next iteration: asyncio.
    try:
        while True:
            amps[0].send(stdout.pop())
    except StopIteration:
        pass

    return stdout.pop()

def part1():
    return max(calculate_max_thrust(phase_settings) for phase_settings in permutations(range(5), 5))

def part2():
    return max(calculate_max_thrust(phase_settings) for phase_settings in permutations(range(5, 10), 5))


if __name__ == '__main__':
    print(part1()) # 46248
    print(part2()) # 54163586
