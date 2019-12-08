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

class TurtleMarker(object):
    def __init__(self):
        self.grid = defaultdict(lambda: defaultdict(lambda: 0))
        self.clashes = dict()
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
        if self.grid[row][col] and self.grid[row][col] != self.colour:
            self.clashes[(row,col)] = self.distance
        self.grid[row][col] = self.colour
    
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
                elif (row, col) in self.clashes:
                    print('X', end='')
                elif self.grid[row][col]:
                    print(self.grid[row][col], end='')
                else:
                    print('.', end='')
            print()


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
    return trace(line1, line2)

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
    #turtle.print_grid()
    print(turtle.clashes)
    return min(map(manhattan_distance, turtle.clashes))
 
if __name__ == '__main__':
    l1 = "R8,U5,L5,D3"
    l2 = "U7,R6,D4,L4"
    result = trace(l1, l2)
    # l1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    # l2 = "U62,R66,U55,R34,D71,R55,D58,R83"
    # result = trace(l1, l2)
    # print(result)
    # print(part1())
