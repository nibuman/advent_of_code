"""AoC 8, 2023: Haunted wasteland."""

# Standard library imports
import pathlib
import sys
import math
from itertools import cycle


def part1(data) -> int:
    directions, dir_map = data
    current_keys = ["AAA"]
    return count_path(directions, dir_map, current_keys, end_p1)[0]


def part2(data) -> int:
    directions, dir_map = data
    current_keys = [key for key in dir_map if key[2] == "A"]
    counts = count_path(directions, dir_map, current_keys, end_p2)
    return math.lcm(*counts)


def count_path(directions, dir_map, current_keys: list[str], end_func):
    rl_map = {"L": 0, "R": 1}
    counts = []
    for idx, current_key in enumerate(current_keys):
        for c, d in enumerate(cycle(directions), start=1):
            val_index = rl_map[d]
            current_vals = dir_map[current_key]
            current_key = current_vals[val_index]
            current_keys[idx] = current_key
            if end_func(current_key):
                counts.append(c)
                break
    return counts


def end_p1(key: str):
    return key == "ZZZ"


def end_p2(key: list[str]):
    return key[2] == "Z"


def parse_data(data: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    dir_map = {}
    directions = ""
    for idx, line in enumerate(data):
        if not idx:
            directions = line
        elif not line:
            continue
        else:
            key, values = line.split(" = ")
            v1, v2 = values.removeprefix("(").removesuffix(")").split(", ")
            dir_map[key] = (v1, v2)
    return directions, dir_map


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
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
