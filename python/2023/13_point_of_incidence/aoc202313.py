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
    return calc_score(data, find_vertical_reflection, find_horizontal_reflection)


def calc_score(data, vertical_func, horizontal_func):
    return sum(vertical_func(puzzle) + 100 * horizontal_func(puzzle) for puzzle in data)


def find_horizontal_reflection(data) -> int:
    previous_row = data[0]
    for r, row in enumerate(data[1::], start=1):
        if (previous_row == row) and check_all_rows(data, r - 1):
            return r
        previous_row = row
    return 0


def check_all_rows(data, row: int) -> bool:
    return all(row1 == row2 for row1, row2 in zip(data[row::-1], data[row + 1 : :]))


def find_vertical_reflection(data) -> int:
    previous_col = [row[0] for row in data]
    for c in range(1, len(data[0])):
        col = [row[c] for row in data]
        if (previous_col == col) and check_all_cols(data, c - 1):
            return c
        previous_col = col
    return 0


def check_all_cols(data, col1: int) -> bool:
    for c1, c2 in zip(range(col1, -1, -1), range(col1 + 1, len(data[0]))):
        if not all(row[c1] == row[c2] for row in data):
            return False
    return True


def part2(data):
    """Solve part 2."""
    return calc_score(data, vertical_reflection_smudge, horizontal_reflection_smudge)


def horizontal_reflection_smudge(data) -> int:
    for r in range(len(data) - 1):
        if count_horizontal_smudges(data, r) == 1:
            return r + 1
    return 0


def vertical_reflection_smudge(data) -> int:
    for c in range(len(data[0])):
        if count_vertical_smudges(data, c) == 1:
            return c + 1
    return 0


def count_vertical_smudges(data, start_col):
    return sum(
        row[c1] != row[c2]
        for c1, c2 in zip(
            range(start_col, -1, -1), range(start_col + 1, len(data[0]), 1)
        )
        for row in data
    )


def count_horizontal_smudges(data, start_row):
    return sum(
        row1[c] != row2[c]
        for row1, row2 in zip(data[start_row::-1], data[start_row + 1 : :])
        for c, _ in enumerate(row1)
    )


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
