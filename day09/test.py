from day09.run import Computer, receive, run_computer

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

def test_computer_relative_mode1():
    program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    output = run_computer([], lambda: list(program))
    assert output == program

def test_computer_large_number1():
    program = [1102,34915192,34915192,7,4,7,99,0]
    output = run_computer([], lambda: list(program))
    assert len(str(output[0])) == 16

def test_computer_large_number2():
    program = [104,1125899906842624,99]
    output = run_computer([], lambda: list(program))
    assert output[0] == 1125899906842624
