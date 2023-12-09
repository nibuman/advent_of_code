"""AoC 3, 2023: Gear ratios."""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass

DIGITS = {str(n) for n in range(10)}
ROW_LENGTH = 0
COL_LENGTH = 0
CURRENT_DATA = []


@dataclass
class Number:
    value: int
    win: list[list[str]] | None = None
    win_row: int | None = None
    win_col: int | None = None


def part1(numbers):
    part_numbers = []
    for number in numbers:
        if adjacent_symbols(number):
            part_numbers.append(number)
    return sum([part_num.value for part_num in part_numbers])


def part2(numbers):
    stars = {
        (r, c): []
        for r in range(ROW_LENGTH)
        for c in range(COL_LENGTH)
        if CURRENT_DATA[r][c] == "*"
    }
    for number in numbers:
        adjacent_stars(number, stars)
    gear_ratios = [p[0] * p[1] for p in stars.values() if len(p) == 2]
    return sum(gear_ratios)


def get_number(row, col, num_buffer, data):
    start_row = row - 1 if row - 1 >= 0 else 0
    start_col = col - 1 if col - 1 >= 0 else 0
    end_row = row + 2
    end_col = col + len(num_buffer) + 1
    win = []
    for row in data[start_row:end_row]:
        win.append(row[start_col:end_col])
    return Number(
        value=int("".join(num_buffer)),
        win=win,
        win_col=start_col,
        win_row=start_row,
    )


def adjacent_symbols(number):
    NON_SYMBOLS = DIGITS | {"."}
    chars_in_window = {char for row in number.win for char in row}
    return chars_in_window - NON_SYMBOLS


def adjacent_stars(number, stars):
    for row_id, row in enumerate(number.win):
        for col_id, char in enumerate(row):
            if char == "*":
                stars[(row_id + number.win_row, col_id + number.win_col)].append(
                    number.value
                )


def numbers_gen(data):
    max_col = len(data[0])
    for row_id, row in enumerate(data):
        num_buffer = []
        for col_id, char in enumerate(row):
            if char in DIGITS:
                num_buffer.append(char)
            elif num_buffer:
                yield get_number(row_id, col_id - len(num_buffer), num_buffer, data)
                num_buffer.clear()
        if num_buffer:
            yield get_number(row_id, col_id - len(num_buffer), num_buffer, data)
            num_buffer.clear()


def parse(data):
    global ROW_LENGTH, COL_LENGTH, CURRENT_DATA
    ROW_LENGTH = len(data)
    COL_LENGTH = len(data[0])
    CURRENT_DATA = data
    return numbers_gen(data)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    yield "Part 1", part1(data)
    data = parse(puzzle_input)
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
