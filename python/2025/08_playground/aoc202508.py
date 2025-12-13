"""AoC 8, 2025: Playground."""

# Standard library imports
from dataclasses import dataclass, field
import pathlib
import sys
from datetime import datetime
import math
from typing import Generator
from itertools import combinations


@dataclass(unsafe_hash=True, frozen=True)
class JunctionBox:
    x: int = field(hash=True)
    y: int = field(hash=True)
    z: int = field(hash=True)
    attachments: list[JunctionBox] = field(default_factory=list, hash=False, init=False)

    def __iter__(self) -> Generator[int, None, None]:
        yield self.x
        yield self.y
        yield self.z

    def __sub__(self, other) -> float:
        return math.dist(self, other)

    def __str__(self):
        return f"x, y, z = {self.x}, {self.y}, {self.z}"


def parse(puzzle_input: str) -> list[JunctionBox]:
    """Parse input."""
    rows = puzzle_input.split("\n")
    return [JunctionBox(*[int(num) for num in row.split(",")]) for row in rows]


def part1(data: list[JunctionBox], data_set: str):
    """Solve part 1."""
    pair_length = {"example1": 10, "input": 1000}[data_set]

    jb_pairs = sorted(list(combinations(data, 2)), key=lambda x: x[0] - x[1])
    jbs = set()

    for first_jb, second_jb in jb_pairs[:pair_length]:
        first_jb.attachments.append(second_jb)
        second_jb.attachments.append(first_jb)
        jbs.update((first_jb, second_jb))

    path_lengths = []
    while jbs:
        jb = jbs.pop()
        jbs.add(jb)
        path_lengths.append(get_path_len(jb, jbs))
    return math.prod(sorted(path_lengths, reverse=True)[0:3])


def get_path_len(jb: JunctionBox, jbs: set) -> int:
    if jb not in jbs:
        return 0
    jbs.discard(jb)
    path_len = 1
    for next_jb in jb.attachments:
        path_len += get_path_len(next_jb, jbs)
    return path_len


def part2(data: list[JunctionBox], data_set: str):
    """Solve part 2."""

    jb_pairs = sorted(list(combinations(data, 2)), key=lambda x: x[0] - x[1])
    jbs = set()
    for first_jb, second_jb in jb_pairs:
        first_jb.attachments.append(second_jb)
        second_jb.attachments.append(first_jb)
        jbs.update((first_jb, second_jb))
        if get_path_len(jb_pairs[-1][0], jbs.copy()) == len(data):
            return first_jb.x * second_jb.x


def solve(puzzle_input, data_set: str):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    for name, func in (("Part1", part1), ("Part2", part2)):
        t1 = datetime.now()
        result = func(data, data_set)
        t2 = datetime.now()
        yield name, result, (t2 - t1).microseconds


def read_file(file_name) -> str:
    PUZZLE_DIR = pathlib.Path(__file__).parent
    return pathlib.Path(PUZZLE_DIR / file_name).read_text().rstrip()


if __name__ == "__main__":
    DEFAULT_INPUT_FILES = ["example1.txt", "input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(
            puzzle_input=read_file(file_name), data_set=file_name.removesuffix(".txt")
        )
        print(
            "\n".join(
                f"{puzzle}: {solution} (in {time / 1000} ms)"
                for puzzle, solution, time in solutions
            )
        )
