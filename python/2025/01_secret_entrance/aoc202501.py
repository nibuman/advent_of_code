"""AoC 1, 2025: Secret Entrance."""

# Standard library imports
import pathlib
import sys
from typing import Generator

START_POS = 50


def parse(puzzle_input):
    """Parse input."""
    return puzzle_input


def rotations(data) -> Generator[tuple[int, int, int]]:
    pos = START_POS
    for d in data:
        direction = d[0]
        distance = int(d[1:])
        if direction == "L":
            distance = -distance
        shift = pos + distance
        pos = shift % 100
        yield pos, shift, distance


def part1(data):
    return sum(pos == 0 for pos, _, _ in rotations(data))


def part2(data):
    """Solve part 2."""
    counts = 0
    old_pos = START_POS
    for pos, shift, distance in rotations(data):
        if distance == 0:
            continue
        if (old_pos != 0) and (shift <= 0):
            counts += abs((shift - 1) // 100)
        else:
            counts += abs(shift) // 100
        old_pos = pos
    return counts


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
