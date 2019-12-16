import os

from collections import defaultdict
from itertools import islice, chain, dropwhile

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input8.txt')
    with open(input_file, 'r') as f:
        for line in f:
            for value in line.strip():
                yield int(value)


def as_rows(length, input):
    while l := list(islice(input, length)):
        yield l

def as_layers(num_rows, num_columns, input):
    while layer := list(islice(as_rows(num_columns, input), num_rows)):
        yield layer

def get_freqs(num_rows, num_columns, input):
    frequencies = {}
    for i, layer in enumerate(as_layers(num_rows, num_columns, input)):
        d = defaultdict(int)
        frequencies[i] = d
        for n in chain(*layer):
            d[n] += 1
    return frequencies

def part1(num_rows, num_columns, input):
    freqs = get_freqs(num_rows, num_columns, input)
    zeros = [(table[0], l) for l, table in freqs.items()]
    layer = min(zeros)[1]
    return freqs[layer][1]*freqs[layer][2]

def part2(num_rows, num_columns, input):
    for row in zip(*as_layers(num_rows, num_columns, input)):
        for pixel in zip(*row):
            result = next(filter(lambda x: x != 2, pixel))
            result = {0: '-', 1: '1'}[result]
            print(result, end='')
        print()

if __name__ == '__main__':
    print(part1(6,25,get_input())) # 1596
    part2(6,25,get_input())
    # 1----111--111---11--1111-
    # 1----1--1-1--1-1--1-1----
    # 1----111--1--1-1----111--
    # 1----1--1-111--1----1----
    # 1----1--1-1-1--1--1-1----
    # 1111-111--1--1--11--1111-
