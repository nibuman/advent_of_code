"""AoC 6, 2023: Wait for it."""

# Standard library imports
import pathlib
import sys
from typing import NamedTuple
import math


class Race(NamedTuple):
    time: int
    distance: int


def part1(data):
    times, distances = data
    races = [Race(time=int(t), distance=int(d)) for t, d in zip(times, distances)]
    return race_calcs(races)


def part2(data):
    times, distances = data
    races = [
        Race(time=int("".join(times)), distance=int("".join(distances))),
    ]
    return race_calcs(races)


def race_calcs(races: list[Race]):
    ways_to_beat_record = []
    for race in races:
        start, stop = solve_quadratic(-1, race.time, -race.distance)
        ways_to_beat_record.append(int(stop - 0.00000000001) - int(start))  # Cringe
    return math.prod(ways_to_beat_record)


def solve_quadratic(a, b, c):
    sqrt_b2_4ac = (b**2 - 4 * a * c) ** 0.5
    return (-b + sqrt_b2_4ac) / (2 * a), (-b - sqrt_b2_4ac) / (2 * a)


def parse(data: list[str]):
    times = data[0].removeprefix("Time:").split()
    distances = data[1].removeprefix("Distance:").split()
    return times, distances


def parse2(data: list[str]):
    times = data[0].removeprefix("Time:").split()
    distances = data[1].removeprefix("Distance:").split()
    return [
        Race(time=int("".join(times)), distance=int("".join(distances))),
    ]


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
