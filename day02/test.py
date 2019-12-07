from day02.run import Computer

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
