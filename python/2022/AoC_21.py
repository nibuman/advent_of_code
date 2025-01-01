from operator import sub, add, mul, floordiv

monkeys = dict()
op_map = {"+": add, "-": sub, "/": floordiv, "*": mul}


def read_file(filename):
    with open(filename, "r") as f:
        return f.read().strip().split("\n")


def parse(file_data):
    global monkeys
    for line in file_data:
        match line.split():
            case [monkey, number]:
                monkeys[monkey[:4]] = int(number)
            case [monkey1, monkey2, operator, monkey3]:
                monkeys[monkey1[:4]] = [monkey2, op_map[operator], monkey3]


def calc(monkey):
    global monkeys
    while True:
        match monkeys[monkey]:
            case int(number):
                return number
            case [int(num1), "=", int(num2)]:
                return num1 - num2
            case [int(num1), operator, int(num2)]:
                monkeys[monkey] = operator(num1, num2)
            case [str(monkey1), operator, monkey2]:
                m1 = calc(monkey1)
                monkeys[monkey] = [m1, operator, monkey2]
            case [monkey1, operator, str(monkey2)]:
                m2 = calc(monkey2)
                monkeys[monkey] = [monkey1, operator, m2]


def try_humn(humn_number):
    global monkeys, original_monkeys
    monkeys = original_monkeys.copy()
    monkeys["root"][1] = "="
    monkeys["humn"] = humn_number
    return calc("root")


def tune(humn, offset):
    diff = try_humn(humn)
    while diff:
        prev_humn = humn
        humn += offset
        diff = try_humn(humn)
        if diff < 0:
            humn = prev_humn
            offset //= 10
    return humn


if __name__ == "__main__":
    file_data = read_file("day21a_data")
    parse(file_data)
    original_monkeys = monkeys.copy()
    print("Part 1: ", calc("root"))
    HUMN_START = 3246000000000
    OFFSET_START = 1000000000
    print("Part 2: ", tune(HUMN_START, OFFSET_START))
