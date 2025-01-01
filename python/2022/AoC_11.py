from dataclasses import dataclass
from operator import add, mul
from math import prod


op_map = {"+": add, "*": mul}


@dataclass
class monkey:
    items: list
    worry_function: callable
    test: int
    true_monkey: int
    false_monkey: int
    inspections: int = 0


def read_file(filename):
    with open(filename, "r") as f:
        return f.read().strip().replace(",", "").split("\n\n")


def parse_notes(monkey_data):
    for line in monkey_data.split("\n"):
        match line.split():
            case ["Starting", "items:", *items]:
                items = [int(item) for item in items]
            case ["Operation:", "new", "=", "old", operator, "old"]:
                function = lambda old: op_map[operator](old, old)
            case ["Operation:", "new", "=", "old", operator, number]:
                function = lambda old: op_map[operator](old, int(number))
            case ["Test:", "divisible", "by", test]:
                test = int(test)
            case ["If", "true:", "throw", "to", "monkey", true_monkey]:
                true_monkey = int(true_monkey)
            case ["If", "false:", "throw", "to", "monkey", false_monkey]:
                false_monkey = int(false_monkey)
    return monkey(items, function, test, true_monkey, false_monkey)


def process_monkey(this_monkey: monkey, part: int):
    for item in this_monkey.items:
        this_monkey.inspections += 1
        worry_level = this_monkey.worry_function(item)
        if part == 1:
            worry_level //= 3
        elif part == 2:
            worry_level %= div_lcm
        if not worry_level % this_monkey.test:
            throw_monkey = this_monkey.true_monkey
        else:
            throw_monkey = this_monkey.false_monkey
        monkeys[throw_monkey].items.append(worry_level)
    this_monkey.items.clear()


def get_inspection_level(part: int, rounds: int) -> int:
    for _ in range(rounds):
        for monkey in monkeys:
            process_monkey(monkey, part)
    return prod(sorted([monkey.inspections for monkey in monkeys])[-2:])


if __name__ == "__main__":
    monkey_notes = read_file("day11a_data")
    monkeys = [parse_notes(monkey) for monkey in monkey_notes]
    div_lcm = prod(monkey.test for monkey in monkeys)
    inspection_level = get_inspection_level(1, 20)
    print("Part 1: ", inspection_level)
    monkeys = [parse_notes(monkey) for monkey in monkey_notes]
    inspection_level = get_inspection_level(2, 10_000)
    print("Part 2: ", inspection_level)
