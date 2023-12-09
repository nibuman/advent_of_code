"""AoC 1, 2023: trebuchet."""

# Standard library imports
import pathlib
import sys


digit_text = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
digit_str = [str(d) for d in range(10)]
number_map = {text: digit for text, digit in zip(digit_text + digit_str, digit_str * 2)}


def part1(data):
    numbers = []
    for line in data:
        digits = [char for char in line if char in "0123456789"]
        numbers.append(int("".join([digits[0], digits[-1]])))
    return sum(numbers)


def part2(data):
    numbers = []
    for line in data:
        digits = []
        for digit in number_map:
            start = 0
            while True:
                try:
                    idx = line.index(digit, start)
                except ValueError:
                    break
                digits.append((idx, number_map[digit]))
                start = idx + len(digit)
        digits = [digit for _, digit in sorted(digits)]
        numbers.append(int("".join([digits[0], digits[-1]])))
    return sum(numbers)


def parse(data):
    return data


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    yield "Part 1", part1(data)
    yield "Part 2", part2(data)


def read_file(file_name):
    PUZZLE_DIR = pathlib.Path(__file__).parent
    return pathlib.Path(PUZZLE_DIR / file_name).read_text().rstrip().split("\n")


if __name__ == "__main__":
    DEFAULT_INPUT_FILES = ["example1.txt", "input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(puzzle_input=read_file(file_name))
        print("\n".join(f"{puzzle}: {solution}" for puzzle, solution in solutions))
