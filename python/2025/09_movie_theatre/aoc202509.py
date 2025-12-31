"""AoC 9, 2025: Movie Theatre."""

# Standard library imports
from dataclasses import dataclass
import pathlib
import sys
from datetime import datetime
import numpy as np
import math
import itertools
from typing import Literal


@dataclass(frozen=True, eq=True)  # With frozen and eq, __hash__ will be implemented
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


def parse(puzzle_input: str) -> list[V]:
    """Parse input."""
    data = puzzle_input.split("\n")
    return [V.from_string(*row.split(",")) for row in data]


def calculate_angle(vec1: V, vec2: V) -> float:
    angle_rad = math.acos((vec1 @ vec2) / (vec1.dist * vec2.dist))
    return math.degrees(angle_rad)


def convex_hull(data: set[V]) -> list[V]:
    p1 = first_point = min(data, key=lambda p: (p.x, p.y))  # left-most point is on cvh
    v1 = V(x=0, y=1)  # Unit vector pointing down. First vector used in measuring angle
    convex_hull = [first_point]
    p3 = V(x=-1, y=-1)  # Just some point that isn't equal to first_point
    while p3 != first_point:
        p3 = min(data, key=lambda p2: calculate_angle(v1, p2 - p1))
        v1 = p3 - p1
        p1 = p3
        data.remove(p1)
        convex_hull.append(p1)
    return convex_hull


def get_direction(v: V) -> Literal["D", "R", "U", "L"]:
    """Return the direction Down, Right, Up, or Left of a vector, assuming that it only changes
    in one dimension
    """
    if v.x < 0:
        return "L"
    elif v.x > 0:
        return "R"
    elif v.y < 0:
        return "U"
    elif v.y > 0:
        return "D"
    raise ValueError("Vector is null")


def is_inside(p1: V, p2: V, p3: V) -> bool:
    """For a clockwise rotation, indicate whether the square where p1, p3, p3 form the first
    3 points will lie (mainly) inside the overall shape
    """
    direction = "".join([get_direction(v) for v in [p2 - p1, p3 - p2]])
    allowed_directions = {"RD", "DL", "LU", "UR"}
    return direction in allowed_directions


def part1(data: list[V]):
    """Solve part 1."""
    set_data = set(data)
    cvh = convex_hull(set_data)
    all_vecs = (p2 - p1 for p1, p2 in itertools.combinations(cvh, 2))
    return max(v.area for v in all_vecs)


def part2(data: list[V]):
    """Solve part 2."""
    areas = []
    for p1, p2, p3 in zip(data, data[1:] + data[:1], data[2:] + data[:2], strict=True):
        if is_inside(p1, p2, p3):
            areas.append((p3 - p1).area)
            print(areas)
    return max(areas)


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
