from collections import defaultdict

def check_range(low, high, validate_func):
    for i in range(low, high+1):
        if validate_func(i):
            yield i

def validate(n: int):
    digits = map(int, str(n))
    prev_digit = None
    found_adj_pair = False
    for digit in digits:
        if prev_digit == digit:
            found_adj_pair = True
        elif prev_digit is not None and prev_digit > digit:
            return False
        prev_digit = digit

    # if we got here, all digits increase left to right
    return found_adj_pair

def validate2(n: int):
    digits = map(int, str(n))
    prev_digit = None
    found_adj_pair = False
    current_run = 1
    for digit in digits:
        # print(f'prev_digit={prev_digit} digit={digit} found_adj_pair={found_adj_pair} current_run={current_run}')
        if prev_digit == digit:
            current_run += 1
        elif prev_digit is not None and prev_digit > digit:
            return False
        else:
            if current_run == 2:
                found_adj_pair = True
            current_run = 1
        prev_digit = digit
    
    # check the final run
    if current_run == 2:
        found_adj_pair = True

    # if we got here, all digits increase left to right
    return found_adj_pair


if __name__ == '__main__':
    # part 1
    print(len(list(check_range(264360, 746325, validate_func=validate)))) # 945
    # part 2
    print(len(list(check_range(264360, 746325, validate_func=validate2)))) # 617
    # print(validate2(112233))
    # print(validate2(123444))
    # print(validate2(111122))
    # print(validate2(112222))
