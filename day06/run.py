from __future__ import annotations # forward reference for recursive definition of Planet

import os

from dataclasses import dataclass, field
from collections import deque

def get_input():
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'input6.txt')
    with open(input_file, 'r') as f:
        for line in f:
            orbitee, orbiter = map(lambda s: s.strip(), line.split(')'))
            yield orbitee, orbiter

@dataclass(unsafe_hash=True)
class Planet:
    name: str
    orbits: Planet = field(compare=False, default=None)
    orbited_by: [Planet] = field(compare=False, default_factory=set)
    COM_distance: int = field(compare=False, default=None)

    def neighbours(self):
        if self.orbits:
            yield self.orbits
        for p in self.orbited_by:
            yield p

def build_planet_map(input):
    planets = {}
    for orbitee, orbiter in input:
        p1 = planets.get(orbitee, Planet(name=orbitee))
        p2 = planets.get(orbiter, Planet(name=orbiter))
        p2.orbits = p1
        p1.orbited_by.add(p2)
        planets[orbitee] = p1
        planets[orbiter] = p2
    return planets

def calculate_COM_distance(planets):
    planets['COM'].COM_distance = 0
    nodes = deque(planets['COM'].orbited_by)
    while nodes:
        node = nodes.popleft()
        nodes.extend(node.orbited_by)
        node.COM_distance = node.orbits.COM_distance + 1

def search_for_santa(planets, source, target_name):
    source.COM_distance = 0
    nodes = deque([(n, 1) for n in source.neighbours()])
    visited = set([source])
    while nodes:
        node, distance = nodes.popleft()
        if node.name == target_name:
            return distance
        if node in visited:
            continue
        visited.add(node)
        distance += 1
        nodes.extend((n, distance) for n in node.neighbours())
        node.COM_distance = distance

def part1(input):
    planets = build_planet_map(input)
    calculate_COM_distance(planets)
    return sum([n.COM_distance for n in planets.values()])

def part2(input):
    planets = build_planet_map(input)
    distance = search_for_santa(planets, planets['YOU'], 'SAN')
    # subtract 2 because we don't count the orbits of santa and you
    return distance - 2

if __name__ == '__main__':
    print(part1(get_input())) # 261306
    print(part2(get_input())) # 382
