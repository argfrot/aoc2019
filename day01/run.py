import os

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input.txt')
    with open(input_file, 'r') as f:
        for line in f:
            yield int(line)

def part1():
    # 3425624
    return sum((value // 3) - 2 for value in get_input())

def get_required_fuel(mass):
    total_fuel = 0
    mass_to_fuel = mass
    while True:
        fuel = (mass_to_fuel // 3) - 2
        if fuel <= 0:
            break
        total_fuel += fuel
        mass_to_fuel = fuel
    return total_fuel

def get_required_fuel_walrus(mass):
    # Maybe the walrus operator has it's uses after all
    total = 0
    while (mass := (mass // 3) - 2) > 0:
        total += mass
    return total


def part2():
    # 5135558
    return sum(get_required_fuel_walrus(mass) for mass in get_input())

if __name__ == '__main__':
    print(part2())
