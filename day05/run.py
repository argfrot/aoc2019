import os

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


class Instruction(object):
    @staticmethod
    def execute(*args):
        pass

class Add(Instruction):
    opcode = Instructions.ADD
    operands = 2
    has_result = True

    @staticmethod
    def execute(*args):
        return args[0] + args[1]

class Mult(Instruction):
    opcode = Instructions.MULT
    operands = 2
    has_result = True

    @staticmethod
    def execute(*args):
        return args[0] * args[1]

STDIN = iter([1])

class Input(Instruction):
    opcode = Instructions.INPUT
    operands = 0
    has_result = True

    @staticmethod
    def execute(*args):
        return next(STDIN)

class Output(Instruction):
    opcode = Instructions.OUTPUT
    operands = 1
    has_result = False

    @staticmethod
    def execute(*args):
        print(args[0])

class End(Instruction):
    opcode = Instructions.END
    operands = 0
    has_result = False

    @staticmethod
    def execute(*args):
        pass

INSTRUCTION_MAP = {
    Instructions.ADD: Add,
    Instructions.MULT: Mult,
    Instructions.INPUT: Input,
    Instructions.OUTPUT: Output,
    Instructions.END: End,
}

class Computer(object):
    def __init__(self, ram):
        self.pc = 0
        self.ram = ram

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
    computer = Computer(ram)
    computer.run()
    return ram[0]

if __name__ == '__main__':
    part1()
