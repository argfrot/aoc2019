from day07.run import Computer, calculate_max_thrust, receive

def test_computer_add():
    ram = [1,0,0,0,99]
    expected_result = [2,0,0,0,99]
    computer = Computer(ram)
    computer.run()
    assert expected_result == ram

def test_computer_mult():
    ram = [2,3,0,3,99]
    expected_result = [2,3,0,6,99]
    computer = Computer(ram)
    computer.run()
    assert expected_result == ram

def test_computer_terminate():
    ram = [2,4,4,5,99,0]
    expected_result = [2,4,4,5,99,9801]
    computer = Computer(ram)
    computer.run()
    assert expected_result == ram

def test_computer_mutate():
    ram = [1,1,1,4,99,5,6,0,99]
    expected_result = [30,1,1,4,2,5,6,0,99]
    computer = Computer(ram)
    computer.run()
    assert expected_result == ram

def test_computer_equal():
    ram = [3,9,8,9,10,9,4,9,99,-1,8]
    input = 8
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [1]

def test_computer_equal2():
    ram = [3,9,8,9,10,9,4,9,99,-1,8]
    input = 9
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [0]

def test_computer_less_than():
    ram = [3,9,7,9,10,9,4,9,99,-1,8]
    input = 7
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [1]

def test_computer_less_than2():
    ram = [3,9,7,9,10,9,4,9,99,-1,8]
    input = 8
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [0]

def test_computer_equal_immediate():
    ram = [3,3,1108,-1,8,3,4,3,99]
    input = 8
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [1]

def test_computer_less_than_immediate():
    ram = [3,3,1107,-1,8,3,4,3,99]
    input = 8
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [0]

def test_computer_jump1():
    ram = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    input = 0
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [0]

def test_computer_jump2():
    ram = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    input = 2
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [1]

def test_computer_jump3():
    ram = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    input = 0
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [0]

def test_computer_jump4():
    ram = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    input = 2
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [1]

def test_computer_long1():
    ram = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
           1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
           999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    input = 8
    stdout = []
    computer = Computer(ram, receive(stdout)).run()
    try:
        computer.send(input)
    except StopIteration:
        pass
    assert stdout == [1000]

def test_max_thrust_1():
    program = lambda: list([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
    result = calculate_max_thrust([4,3,2,1,0], program)
    assert result == 43210

def test_max_thrust_2():
    program = lambda: list([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0])
    result = calculate_max_thrust([0,1,2,3,4], program)
    assert result == 54321

def test_max_thrust_3():
    program = lambda: list([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
    result = calculate_max_thrust([1,0,4,3,2], program)
    assert result == 65210

def test_max_thrust_part2_1():
    program=lambda: list([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
    result = calculate_max_thrust([9,8,7,6,5], program)
    assert result == 139629729

def test_max_thrust_part2_2():
    program=lambda: list([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
    result = calculate_max_thrust([9,7,8,5,6], program)
    assert result == 18216