import os
import math

from collections import defaultdict

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input10.txt')
    with open(input_file, 'r') as f:
        for row, line in enumerate(f):
            for col, value in enumerate(line.strip()):
                if value != '.':
                    yield (row, col)

def test_input_stream(test_data):
    for row, line in enumerate(test_data.splitlines()[1:]):
        for col, value in enumerate(line.strip()):
            if value != '.':
                yield (row, col)

def test_input():
    test_data = """
        .#..#
        .....
        #####
        ....#
        ...##
    """
    return test_input_stream(test_data)

def test_input2():
    test_data = """
        ......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####
    """
    return test_input_stream(test_data)

def test_input3():
    test_data = """
        .#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##
    """
    return test_input_stream(test_data)


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
                print('#', end='')
            else:
                print('.', end='')
        print()


def part1(input=get_input, display=False):
    points = list(input())
    visible_points = {}
    for source_row, source_col in points:
        angles = set()
        for target_row, target_col in points:
            if target_row == source_row and target_col == source_col:
                continue
            delta_x = (target_col - source_col)
            delta_y = (target_row - source_row)
            angle = math.atan2(delta_x, delta_y)
            angles.add(angle)
        visible_points[(source_row, source_col)] = len(angles)
    
    best_position = sorted(visible_points, key=lambda x: visible_points[x], reverse=True)
    if display:
        to_grid(visible_points, best_position[0])
    return best_position[0], visible_points[best_position[0]]


def part2(input=get_input, display=False):
    monitoring_station, _ = part1(input=input, display=display)

    points = list(input())
    points.remove(monitoring_station)
    points = sorted(points, key=lambda p: (p[0] - monitoring_station[0])**2 + (p[1] - monitoring_station[1])**2)

    source_row, source_col = monitoring_station
    vapourised = []

    while points:
        angles = defaultdict(list)
        for target_row, target_col in points:
            delta_x = (target_col - source_col)
            delta_y = (target_row - source_row)
            angle = math.atan2(delta_x, delta_y)
            angles[angle].append((target_row, target_col))

        for angle in sorted(angles, reverse=True):
            v = min(angles[angle], key=lambda p: (p[0] - monitoring_station[0])**2 + (p[1] - monitoring_station[1])**2)
            vapourised.append(v)
            points.remove(v)

    return vapourised[199] # zero-based => 200th item

if __name__ == '__main__':
    # print(part1(input=test_input2)) # ((8, 5), 33)
    # print(part1(input=test_input3)) # ((13, 11), 210)
    # print(part2(input=test_input3)) # (2, 8)

    print(part1()) # ((29, 26), 299)
    print(part2()) # (19, 14)
