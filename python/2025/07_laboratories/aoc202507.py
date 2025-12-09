"""AoC 7, 2025: Laboratories."""

# Standard library imports
import pathlib
import sys
from collections import deque
from itertools import product

type position = tuple[int, int]


def parse(puzzle_input: str) -> tuple[position, set[position], int, int]:
    """Parse input."""
    data = puzzle_input.split("\n")
    r_max = len(data)
    c_max = len(data[0])
    positions = product(range(r_max), range(c_max))
    splitters = {(r, c) for r, c in positions if data[r][c] == "^"}
    start = (0, data[0].find("S"))
    return start, splitters, r_max, c_max


def part1(data):
    """Solve part 1."""
    start, splitters, max_len, max_col = data
    splits = 0
    beams = deque([start])
    row = 0
    split_positions = [(1, -1), (1, 1)]
    while row < max_len + 1:
        row, col = beams.popleft()
        if (row + 1, col) in splitters:
            splits += 1
            for row_shift, col_shift in split_positions:
                new_row = row + row_shift
                new_col = col + col_shift
                if 0 > new_col > max_col:
                    continue
                if (new_row, new_col) not in beams:
                    beams.append((new_row, new_col))
        elif (row + 1, col) not in beams:
            beams.append((row + 1, col))
    return splits


def part2(data):
    """Solve part 2."""


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    yield "Part 1", part1(data)
    yield "Part 2", part2(data)


def read_file(file_name) -> str:
    PUZZLE_DIR = pathlib.Path(__file__).parent
    return pathlib.Path(PUZZLE_DIR / file_name).read_text().rstrip()


if __name__ == "__main__":
    DEFAULT_INPUT_FILES = ["example1.txt", "input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(puzzle_input=read_file(file_name))
        print("\n".join(f"{puzzle}: {solution}" for puzzle, solution in solutions))
