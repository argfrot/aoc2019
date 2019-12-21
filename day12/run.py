import os
import re
import operator

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Any, List

# <x=5, y=-1, z=5>
COORD = '([A-Za-z]*)=(-?[0-9]*)'
FORMAT = re.compile(f'<{COORD}, {COORD}, {COORD}>')
def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input12.txt')
    with open(input_file, 'r') as f:
        for line in f:
            groups = FORMAT.match(line.strip()).groups()
            d = {name: value for name, value in pairs(groups)}
            yield d

def test_input():
    test_data = """
        <x=-1, y=0, z=2>
        <x=2, y=-10, z=-7>
        <x=4, y=-8, z=8>
        <x=3, y=5, z=-1>
    """
    for line in test_data.splitlines():
        if line.strip():
            groups = FORMAT.match(line.strip()).groups()
            d = {name: value for name, value in pairs(groups)}
            yield d

def test_input2():
    test_data = """
        <x=-8, y=-10, z=0>
        <x=5, y=5, z=10>
        <x=2, y=-7, z=3>
        <x=9, y=-8, z=-3>
    """
    for line in test_data.splitlines():
        if line.strip():
            groups = FORMAT.match(line.strip()).groups()
            d = {name: value for name, value in pairs(groups)}
            yield d

def pairs(iterable):
    it = iter(iterable)
    try:
        while True:
            name = next(it)
            value = int(next(it))
            yield (name, value)
    except StopIteration:
        pass

@dataclass
class Moon:
    position: List[int]
    velocity: List[int] = field(default_factory=lambda: list([0,0,0]))

    def apply_gravity(self, other):
        for dimension, (pos, other_pos) in enumerate(zip(self.position, other.position)):
            if pos > other_pos:
                self.velocity[dimension] -= 1
            elif pos < other_pos:
                self.velocity[dimension] += 1

    def move(self):
        self.position = list(map(operator.add, self.position, self.velocity))
    
    def potential_energy(self):
        return sum(map(abs, self.position))

    def kinetic_energy(self):
        return sum(map(abs, self.velocity))

def part1(steps=10, input=get_input, display=False):
    moons = [Moon([v['x'], v['y'], v['z']]) for v in input()]
    step = 1
    while step <= steps:
        if display: print(f'Step {step}:')
        for moon in moons:
            for other_moon in moons:
                if moon != other_moon:
                    moon.apply_gravity(other_moon)
        for moon in moons:
            moon.move()
            if display: print(f'moon={moon} pot={moon.potential_energy()} kin={moon.kinetic_energy()}')
        step += 1
    return sum((moon.potential_energy() * moon.kinetic_energy() for moon in moons))

if __name__ == '__main__':
    print(part1(steps=10, input=test_input)) # 179
    print(part1(steps=100, input=test_input2)) # 1940
    print(part1(steps=1000)) # 7928
