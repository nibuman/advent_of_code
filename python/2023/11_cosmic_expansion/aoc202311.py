"""AoC 11, 2023: Cosmic Expansion."""

# Standard library imports
import pathlib
import sys
from utils.points import Point as P
from utils.points import manhattan


def parse(puzzle_input):
    """Parse input."""
    return [list(row) for row in puzzle_input]


def part1(data: list[list[str]]):
    """Solve part 1."""
    empty_rows = find_empty_rows(data)
    empty_cols = find_empty_cols(data)
    galaxies = find_galaxies(data)
    inflate_space(data, empty_rows, empty_cols, galaxies)
    galaxy_combinations = [(g1, g2) for g1 in range(len(galaxies)) for g2 in range(g1+1, len(galaxies))]
    return sum(manhattan(galaxies[g1], galaxies[g2]) for g1, g2 in galaxy_combinations)
    
def find_empty_rows(data) -> set[int]:
    empty_space = set()
    for r, row in enumerate(data):
        if all(char == "." for char in row):
            empty_space.add(r)
    return empty_space

def find_empty_cols(data) -> set[int]:
    empty_cols=  set()
    for c in range(len(data[0])):
        if all(row[c] == "." for row in data):
            empty_cols.add(c)
    return empty_cols

def inflate_space(data, empty_rows, empty_cols, galaxies, inflation_factor=1):
    for galaxy in galaxies:
        galaxy.row += sum(empty_row < galaxy.row for empty_row in empty_rows) * inflation_factor
        galaxy.col += sum(empty_col < galaxy.col for empty_col in empty_cols) * inflation_factor
        
    # EMPTY_ROW = ["."] * len(data[0])
    # for r in range(len(data), -1, -1):
    #     if r in empty_rows:
    #         data.insert(r, EMPTY_ROW)
    # for c in range(len(data[0]), -1, -1):
    #     if c in empty_cols:
    #         for row in data:
    #             row.insert(c, ".")
                   

def find_galaxies(data) -> list[P]:
    galaxies = []
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if char == "#":
                galaxies.append(P(r,c))
    return galaxies

    


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
