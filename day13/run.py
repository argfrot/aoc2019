import os
import sys

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Any

from itertools import permutations

from day09.run import execute, coroutine

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input13.txt')
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
    os.system('cls' if os.name == 'nt' else 'clear')
    min_row, max_row, min_col, max_col = get_bounds(points)
    for row in range(min_row, max_row+1):
        for col in range(min_col, max_col+1):
            if (row, col) == highlight:
                print('@', end='')
            elif (row, col) in points:
                print(' ~#=*'[points[(row, col)]], end='')
            else:
                print(' ', end='')
        print()

@coroutine
def receive(display, score_container, ball_location, paddle_location):
    while True:
        col = yield
        row = yield
        tile = yield
        if (row, col) == (0, -1):
            score_container[0] = tile
        else:
            display[(row, col)] = tile

        if tile == 4: # the ball
            ball_location[0] = row
            ball_location[1] = col
        elif tile == 3: # the paddle
            paddle_location[0] = row
            paddle_location[1] = col

def run_computer(get_program=get_input, wait_for_input=False):
    score = [0]
    ball = [None, None]
    paddle = [None, None]
    board = defaultdict(int)
    out = receive(board, score, ball, paddle)

    computer = execute(get_program, out, init_ram={0: 2})
    try:
        while True and wait_for_input:
            to_grid(board)
            print(score[0])
            if ball[1] > paddle[1]:
                computer.send(1)
            elif ball[1] < paddle[1]:
                computer.send(-1)
            else:
                computer.send(0)
    except StopIteration:
        pass

    to_grid(board)
    print(score[0])

    number_of_blocks = len([t for t in board.values() if t == 2])
    return number_of_blocks

def part1():
    return run_computer()

def part2():
    return run_computer(wait_for_input=True)


if __name__ == '__main__':
    print(part1()) # 277
    part2() # 12856

