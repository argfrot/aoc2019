import os

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input2.txt')
    with open(input_file, 'r') as f:
        for line in f:
            for value in line.split(','):
                yield int(value)

class Instuctions(object):
    ADD = 1
    MULT = 2
    END = 99

OPERATIONS = {
    Instuctions.ADD: lambda x,y: x+y,
    Instuctions.MULT: lambda x,y: x*y,
}

class Computer(object):
    def __init__(self, ram):
        self.pc = 0
        self.ram = ram

    def run(self):
        while (instruction := self.ram[self.pc]) != Instuctions.END:
            operand1 = self.ram[self.pc+1]
            operand2 = self.ram[self.pc+2]
            target = self.ram[self.pc+3]
            operation = OPERATIONS[instruction]
            self.ram[target] = operation(self.ram[operand1], self.ram[operand2])
            self.pc += 4

def part1(noun, verb):
    ram = list(get_input())
    ram[1] = noun
    ram[2] = verb
    computer = Computer(ram)
    computer.run()
    return ram[0]

def part2():
    target = 19690720
    for noun in range(100):
        for verb in range(100):
            if part1(noun, verb) == target:
                return noun*100 + verb


if __name__ == '__main__':
    print(part2())
