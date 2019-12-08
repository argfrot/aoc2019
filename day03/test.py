from day03.run import trace

def test_basic():
    l1 = "R8,U5,L5,D3"
    l2 = "U7,R6,D4,L4"
    assert trace(l1, l2) == 6

def test_example1():
    l1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    l2 = "U62,R66,U55,R34,D71,R55,D58,R83"
    assert trace(l1, l2) == 159

def test_example2():
    l1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    l2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
    assert trace(l1, l2) == 135
