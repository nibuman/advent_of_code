"""AoC 13, 2023: Point of incidence."""

# Standard library imports
import pathlib
import sys


def parse(puzzle_input):
    """Parse input."""
    puzzle = []
    puzzles = []
    for row in puzzle_input:
        if row:
            puzzle.append(row)
        else:
            puzzles.append(puzzle.copy())
            puzzle.clear()
    puzzles.append(puzzle)
    return puzzles


def part1(data):
    """Solve part 1."""
    scores = []
    for puzzle in data:
        h = find_horizontal_reflection(puzzle)
        v = find_vertical_reflection(puzzle)
        if h:
            scores.append(h * 100)
        if v:
            scores.append(v)
    return sum(scores)


def find_horizontal_reflection(data) -> int | None:
    previous_row = None
    for r, row in enumerate(data):
        if (previous_row == row) and check_all_rows(data, r - 1):
            return r
        previous_row = row
    return None


def check_all_rows(data, row1: int) -> bool:
    return all(
        data[r1] == data[r2]
        for r1, r2 in zip(range(row1, -1, -1), range(row1 + 1, len(data), 1))
    )


def find_vertical_reflection(data) -> int | None:
    previous_col = None
    for c in range(len(data[0])):
        col = [row[c] for row in data]
        if (previous_col == col) and check_all_cols(data, c - 1):
            return c
        previous_col = col
    return None


def check_all_cols(data, col1: int) -> bool:
    for c1, c2 in zip(range(col1, -1, -1), range(col1 + 1, len(data[0]))):
        if not all(row[c1] == row[c2] for row in data):
            return False
    return True


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
