"""AoC 9, 2025: Movie Theatre."""

# Standard library imports
from dataclasses import dataclass
import pathlib
import sys
from datetime import datetime
import numpy as np
import math
import itertools


@dataclass(frozen=True, eq=True)
class V:
    x: int
    y: int

    @property
    def dist(self):
        return math.hypot(self.x, self.y)

    @property
    def area(self):
        return (abs(self.x) + 1) * (abs(self.y) + 1)

    @property
    def _np(self) -> np.typing.NDArray[np.int64]:
        return np.array([self.x, self.y])

    def __add__(self, other: V) -> V:
        return V(x=(self.x + other.x), y=(self.y + other.y))

    def __sub__(self, other: V) -> V:
        return V(x=(self.x - other.x), y=(self.y - other.y))

    def __matmul__(self, other: V):
        return self._np @ other._np

    @classmethod
    def from_string(cls, x: str, y: str) -> V:
        return cls(x=int(x), y=int(y))


def parse(puzzle_input: str) -> set[V]:
    """Parse input."""
    data = puzzle_input.split("\n")
    return {V.from_string(*row.split(",")) for row in data}


def calculate_angle(vec1: V, vec2: V) -> float:
    angle_rad = math.acos((vec1 @ vec2) / (vec1.dist * vec2.dist))
    return math.degrees(angle_rad)


def convex_hull(data: set[V]) -> list[V]:
    first_point = min(data, key=lambda p: (p.x, p.y))
    v1 = V(x=0, y=1)  # Unit vector pointing down. First vector used in measuring angle
    convex_hull = [first_point]
    p1 = first_point
    p3 = V(x=first_point.x + 1, y=0)  # Just some point that isn't equal to first_point
    data.remove(first_point)  # first_point needs to be removed for the first iteration
    while p3 != first_point:
        p3 = min(data, key=lambda p2: calculate_angle(v1, p2 - p1))
        data.add(first_point)  # loop will not exit if first_point isn't present
        v1 = p3 - p1
        p1 = p3
        data.discard(p1)
        convex_hull.append(p1)
    return convex_hull


def part1(data: set[V]):
    """Solve part 1."""
    cvh = convex_hull(data)
    all_vecs = (p2 - p1 for p1, p2 in itertools.combinations(cvh, 2))
    return max(v.area for v in all_vecs)


def part2(data):
    """Solve part 2."""


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    for name, func in (("Part1", part1), ("Part2", part2)):
        t1 = datetime.now()
        result = func(data)
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
        solutions = solve(puzzle_input=read_file(file_name))
        print(
            "\n".join(
                f"{puzzle}: {solution} (in {time / 1000} ms)"
                for puzzle, solution, time in solutions
            )
        )
