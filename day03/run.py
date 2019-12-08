import os
from collections import defaultdict

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input3.txt')
    with open(input_file, 'r') as f:
        for line in f:
            yield line

class Direction(object):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Cell(object):
    def __init__(self):
        self.tracks = {}

    def colour_clashes(self, colour):
        # check if this cell is already coloured in a different colour.
        return self.tracks and colour not in self.tracks

    def add_track(self, colour, distance):
        if colour not in self.tracks:
            self.tracks[colour] = distance

    def __str__(self):
        if not self.tracks:
            return '.'
        elif len(self.tracks) > 1:
            return 'X'
        else:
            for key in self.tracks:
                return str(key)

class TurtleMarker(object):
    def __init__(self):
        self.grid = defaultdict(lambda: defaultdict(lambda: Cell()))
        self.clashes = set()
        self.row, self.col = (0, 0)
        self.colour = 0
        self.distance = 0

    def reset_distance(self):
        self.distance = 0

    def jump_to(self, row, col):
        self.row, self.col = (row, col)
    
    def set_colour(self, colour):
        self.colour = colour

    def visit(self, row, col):
        if self.grid[row][col].colour_clashes(self.colour):
            self.clashes.add((row,col))
        self.grid[row][col].add_track(self.colour, self.distance)
    
    def move_one(self, direction):
        self.distance += 1
        if direction == Direction.UP:
            self.row += 1
        elif direction == Direction.RIGHT:
            self.col += 1
        elif direction == Direction.DOWN:
            self.row -= 1
        elif direction == Direction.LEFT:
            self.col -= 1
        self.visit(self.row, self.col)

    def move(self, direction, distance):
        while distance > 0:
            self.move_one(direction)
            distance -= 1

    def get_bounds(self):
        min_row, max_row, min_col, max_col = 0, 0, 0, 0
        for row in self.grid: 
            min_row = min(row, min_row)
            max_row = max(row, max_row)
            for col in self.grid[row]:
                min_col = min(col, min_col)
                max_col = max(col, max_col)
        return min_row, max_row, min_col, max_col

    def print_grid(self):
        min_row, max_row, min_col, max_col = self.get_bounds()
        for row in range(max_row, min_row-1, -1):
            print(f'{row:03}: ', end='')
            for col in range(min_col, max_col+1):
                if (row, col) == (0,0):
                    print('O', end='')
                else:
                    print(self.grid[row][col], end='')
            print()

    def get_clash_distances(self):
        return (self.grid[row][col].tracks for (row, col) in self.clashes)


DIRECTION_LOOKUP = {
    'U' : Direction.UP,
    'R' : Direction.RIGHT,
    'D' : Direction.DOWN,
    'L' : Direction.LEFT,
}

def tokenize(line):
   for move in line.split(','):
        direction = DIRECTION_LOOKUP[move[0]]
        distance = int(move[1:])
        yield (direction, distance)

def manhattan_distance(position):
    row, col = position
    return abs(row) + abs(col)

def part1():
    line1, line2 = get_input()
    return min_manhattan(line1, line2)

def part2():
    line1, line2 = get_input()
    return min_trace_distance(line1, line2)

def min_manhattan(line1, line2):
    turtle = trace(line1, line2)
    return min(map(manhattan_distance, turtle.clashes))

def min_trace_distance(line1, line2):
    turtle = trace(line1, line2)
    return min(map(lambda tracks: sum(tracks.values()), turtle.get_clash_distances()))

def trace(line1, line2):
    turtle = TurtleMarker()
    turtle.set_colour(1)
    for direction, distance in tokenize(line1):
        turtle.move(direction, distance)
    turtle.jump_to(0,0)
    turtle.set_colour(2)
    turtle.reset_distance()
    for direction, distance in tokenize(line2):
        turtle.move(direction, distance)
    return turtle

 
if __name__ == '__main__':
    print(part1()) # 1264
    print(part2()) # 37390
