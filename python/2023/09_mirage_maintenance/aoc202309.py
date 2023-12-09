"""AoC 9, 2023: Mirage Maintenance."""

# Standard library imports
import pathlib
import sys


def parse(puzzle_input):
    """Parse input."""
    return [[int(num) for num in line.split()] for line in puzzle_input]


def part1(data):
    """Solve part 1."""
    return extrapolated_values(data, p1_extrapolation)


def p1_extrapolation(sequence_solver):
    """Take the sum of the end numbers in the sequence"""
    return sum(seq[-1] for seq in sequence_solver)


def p2_extrapolation(sequence_solver):
    """Take the first numbers from each list, make alternate ones negative, then take the sum"""
    first_col = [line[0] for line in sequence_solver]
    for idx, num in enumerate(first_col):
        if idx % 2:
            first_col[idx] = num * -1
    return sum(first_col)


def extrapolated_values(data, extrapolation_func):
    extrapolated_values = []
    for value_history in data:
        sequence_solver = [value_history]
        while any(sequence_solver[-1]):
            next_sequence = []
            for a, b in zip(sequence_solver[-1][:-1], sequence_solver[-1][1:]):
                next_sequence.append(b - a)
            sequence_solver.append(next_sequence)
        extrapolated_values.append(extrapolation_func(sequence_solver))
    return sum(extrapolated_values)


def part2(data):
    """Solve part 2."""
    return extrapolated_values(data, p2_extrapolation)


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
