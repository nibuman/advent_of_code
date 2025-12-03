"""AoC 3, 2025: Lobby."""

# Standard library imports
import pathlib
import sys


def parse(puzzle_input):
    """Parse input."""
    return puzzle_input


def part1(data: list[str]):
    """Solve part 1."""
    joltage: list[int] = []
    for num_str in data:
        num1 = max(num_str[:-1])
        i = num_str.find(num1) + 1
        num2 = max(num_str[i:])
        joltage.append(int(f"{num1}{num2}"))
    return sum(joltage)


def part2(data):
    """Solve part 2."""


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
