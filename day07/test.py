from day07.run import Computer, calculate_max_thrust

def test_computer_add():
    ram = [1,0,0,0,99]
    expected_result = [2,0,0,0,99]
    try:
        computer = Computer(ram).run()
        computer.send(None)
    except StopIteration:
        pass
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
    stdin = iter([8])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [1]

def test_computer_equal2():
    ram = [3,9,8,9,10,9,4,9,99,-1,8]
    stdin = iter([9])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [0]

def test_computer_less_than():
    ram = [3,9,7,9,10,9,4,9,99,-1,8]
    stdin = iter([7])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [1]

def test_computer_less_than2():
    ram = [3,9,7,9,10,9,4,9,99,-1,8]
    stdin = iter([8])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [0]

def test_computer_equal_immediate():
    ram = [3,3,1108,-1,8,3,4,3,99]
    stdin = iter([8])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [1]

def test_computer_less_than_immediate():
    ram = [3,3,1107,-1,8,3,4,3,99]
    stdin = iter([8])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [0]

def test_computer_jump1():
    ram = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    stdin = iter([0])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [0]

def test_computer_jump2():
    ram = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    stdin = iter([2])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [1]

def test_computer_jump3():
    ram = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    stdin = iter([0])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [0]

def test_computer_jump4():
    ram = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
    stdin = iter([2])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
    assert stdout == [1]

def test_computer_long1():
    ram = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
           1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
           999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    stdin = iter([8])
    stdout = []
    computer = Computer(ram, stdin, stdout)
    computer.run()
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
