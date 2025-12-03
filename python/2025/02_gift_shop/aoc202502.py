"""AoC 2, 2025: Gift shop."""

# Standard library imports
import pathlib
import sys
from typing import Generator


def parse(puzzle_input: list[str]) -> str:
    return puzzle_input[0]


def ID_ranges(data: str) -> Generator[tuple[int, int]]:
    """Parse input."""
    for prod_ID_range in data.split(","):
        start, end = prod_ID_range.split("-")
        yield int(start), int(end)


def part1(data: str):
    """Solve part 1."""
    invalid_IDs: list[int] = []
    for start, end in ID_ranges(data):
        for prod_id in range(start, end + 1):
            prod_string = str(prod_id)
            if len(prod_string) % 2 == 1:
                continue
            mid = len(prod_string) // 2
            if prod_string[:mid] == prod_string[mid:]:
                invalid_IDs.append(prod_id)
    return sum(invalid_IDs)


def part2(data):
    """Solve part 2."""
    invalid_IDs: list[int] = []
    for start, end in ID_ranges(data):
        for prod_id in range(start, end + 1):
            prod_string = str(prod_id)
            if len(prod_string) % 2 == 1:
                continue
            mid = len(prod_string) // 2
            if prod_string[:mid] == prod_string[mid:]:
                invalid_IDs.append(prod_id)
    return sum(invalid_IDs)

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
