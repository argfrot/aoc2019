import os

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Any

from itertools import permutations

from day09.run import execute, receive

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input11.txt')
    with open(input_file, 'r') as f:
        for line in f:
            for value in line.split(','):
                yield int(value)

def get_bounds(points):
    min_row, max_row, min_col, max_col = None, None, None, None
    for row, col in points:
        min_row = min(row, min_row) if min_row is not None else row
        max_row = max(row, max_row) if max_row is not None else row
        min_col = min(col, min_col) if min_col is not None else col
        max_col = max(col, max_col) if max_col is not None else col
    return min_row, max_row, min_col, max_col

def to_grid(points, highlight=None):
    min_row, max_row, min_col, max_col = get_bounds(points)
    # print(f'min_row={min_row} max_row={max_row} min_col={min_col} max_col={max_col}')
    for row in range(min_row, max_row+1):
        for col in range(min_col, max_col+1):
            if (row, col) == highlight:
                print('@', end='')
            elif (row, col) in points:
                # print(points[(row, col)], end='')
                if points[(row, col)] == 1:
                    print('#', end='')
                else:
                    print('.', end='')
            else:
                print('.', end='')
        print()

class Direction(object):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def turn_left(direction):
    return (direction - 1) % 4

def turn_right(direction):
    return (direction + 1) % 4

def move_forward(positon, direction):
    row, col = positon
    if direction == Direction.NORTH:
        return (row-1, col)
    elif direction == Direction.EAST:
        return (row, col+1)
    elif direction == Direction.SOUTH:
        return (row+1, col)
    elif direction == Direction.WEST:
        return (row, col-1)
    else:
        raise Exception("Whaaaaat...")

def run_computer(start_colour, get_program=get_input, display=False):
    stdout = []
    out = receive(stdout)

    panels = defaultdict(int)
    position = (0,0)
    direction = Direction.NORTH
    panels[position] = start_colour

    computer = execute(get_program, out)
    try:
        while True:
            computer.send(panels[position])
            paint = stdout.pop(0)
            turn = stdout.pop(0)
            panels[position] = paint
            direction = turn_left(direction) if turn == 0 else turn_right(direction)
            position = move_forward(position, direction)
    except StopIteration:
        pass

    if display:
        to_grid(panels)

    return len(panels)

def part1():
    return run_computer(0)

def part2():
    return run_computer(1, display=True)

if __name__ == '__main__':
    print(part1()) # 2238
    print(part2()) # 249
    # .###..#..#.####.###...##..####.###..###....
    # .#..#.#.#..#....#..#.#..#....#.#..#.#..#...
    # .#..#.##...###..#..#.#..#...#..#..#.#..#...
    # .###..#.#..#....###..####..#...###..###....
    # .#....#.#..#....#....#..#.#....#.#..#......
    # .#....#..#.#....#....#..#.####.#..#.#......
