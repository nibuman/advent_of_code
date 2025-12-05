"""AoC 4, 2025: Building Department."""

# Standard library imports
from os import initgroups
import pathlib
import sys
from itertools import chain


def parse(puzzle_input):
    """Parse input."""
    return puzzle_input


def remove_accessible_rolls(data: list[str]) -> list[str]:
    new_data = data.copy()
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if char == ".":
                continue
            rows = data[r - 1 if r >= 1 else 0 : r + 2]
            window = [row[c - 1 if c >= 1 else 0 : c + 2] for row in rows]
            if "".join(chain(window)).count("@") < 5:
                new_data[r] = f"{new_data[r][:c]}.{new_data[r][c + 1 :]}"
    return new_data


def part1(data: list[str]):
    """Solve part 1."""
    removed = remove_accessible_rolls(data)
    initial_count = "".join(chain(data)).count("@")
    removed_count = "".join(chain(removed)).count("@")
    return initial_count - removed_count


def part2(data):
    """Solve part 2."""
    initial_count = "".join(chain(data)).count("@")
    old_count = initial_count + 1
    new_count = initial_count
    while old_count > new_count:
        data = remove_accessible_rolls(data)
        old_count = new_count
        new_count = "".join(chain(data)).count("@")
    return initial_count - new_count


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    yield "Part 1", part1(data)
    yield "Part 2", part2(data)


def read_file(file_name) -> list[str]:
    PUZZLE_DIR = pathlib.Path(__file__).parent
    return pathlib.Path(PUZZLE_DIR / file_name).read_text().rstrip().split("\n")


if __name__ == "__main__":
    DEFAULT_INPUT_FILES = ["example1.txt", "input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(puzzle_input=read_file(file_name))
        print("\n".join(f"{puzzle}: {solution}" for puzzle, solution in solutions))
