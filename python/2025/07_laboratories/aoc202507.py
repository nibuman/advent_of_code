"""AoC 7, 2025: Laboratories."""

# Standard library imports
import functools
import pathlib
import sys
from collections import deque
from itertools import product
from typing import Final

position = tuple[int, int]
SPLITTERS: Final[frozenset[position]]
R_MAX: Final[int]
C_MAX: Final[int]
seen_splitters = set()


def parse(puzzle_input: str) -> position:
    """Parse input."""
    global SPLITTERS, R_MAX, C_MAX
    data = puzzle_input.split("\n")
    R_MAX = len(data)
    C_MAX = len(data[0])
    positions = product(range(R_MAX), range(C_MAX))
    SPLITTERS = frozenset((r, c) for r, c in positions if data[r][c] == "^")
    start = (0, data[0].find("S"))
    return start


def part1(data):
    """Solve part 1."""
    return count_splits(pos=data)


def count_splits(pos: position) -> int:
    """Given a beam position, works out what the next positions and returns the number
    of splits
    """
    splits = 0
    r, c = pos
    if r >= R_MAX:
        return 0
    if 0 > c >= C_MAX:
        return 0
    if (r, c) in seen_splitters:
        return 0
    if (r, c) in SPLITTERS:
        seen_splitters.add((r, c))
        splits = 1
        splits += count_splits(pos=(r + 1, c + 1))
        splits += count_splits(pos=(r + 1, c - 1))
    else:
        splits += count_splits(pos=(r + 1, c))
    return splits


@functools.cache
def follow_beam(pos: position) -> int:
    """Given a beam position, works out what the next positions and returns the number
    of beams that reach the end
    """
    beam_count = 0
    r, c = pos
    if r >= R_MAX:
        return 1
    if 0 > c >= C_MAX:
        return 0
    if (r, c) in SPLITTERS:
        beam_count += follow_beam(pos=(r + 1, c + 1))
        beam_count += follow_beam(pos=(r + 1, c - 1))
    else:
        beam_count += follow_beam(pos=(r + 1, c))
    return beam_count


def part2(data):
    """Solve part 2."""
    return follow_beam(pos=data)


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
