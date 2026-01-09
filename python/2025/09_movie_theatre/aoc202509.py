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


Rectangle = tuple[V, V]
Edge = tuple[V, V]


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


def rectangles_intersect(rect: Rectangle, outside_rectangle: Rectangle) -> bool: ...


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


def corner_direction(p1: V, p2: V, p3: V) -> str:
    return "".join([get_direction(v) for v in [p2 - p1, p3 - p2]])


def point_in_rectangle(p: V, rect: Rectangle) -> bool:
    r1, r2 = rect
    x_min, x_max = min([r1.x, r2.x]), max([r1.x, r2.x])
    y_min, y_max = min([r1.y, r2.y]), max([r1.y, r2.y])
    return (x_min <= p.x <= x_max) and (y_min <= p.y <= y_max)


def part1(data: list[V]):
    """Solve part 1."""
    set_data = set(data)
    cvh = convex_hull(set_data)
    all_vecs = (p2 - p1 for p1, p2 in itertools.combinations(cvh, 2))
    return max(v.area for v in all_vecs)


def get_outside_points(data: list[V]) -> list[V]:
    outside_points: list[V] = []
    offset: dict[str, tuple[V, ...]] = {
        "UL": (V(-1, 1),),
        "RU": (V(-1, -1),),
        "DR": (V(1, -1),),
        "LD": (V(1, 1),),
        "RD": (V(0, -1), V(1, 0)),
        "UR": (V(-1, 0), V(0, -1)),
        "LU": (V(0, 1), V(-1, 0)),
        "DL": (V(1, 0), V(0, 1)),
    }
    for p1, p2, p3 in zip(data, data[1:] + data[:1], data[2:] + data[:2]):
        direction = corner_direction(p1, p2, p3)
        outside_points.extend([p2 + dV for dV in offset[direction]])
    return outside_points


def get_edges(data: list[V]) -> tuple[list[Edge], list[Edge]]:
    vertical_points: list[Edge] = []
    horizontal_points: list[Edge] = []
    for p1, p2 in zip(data, data[1:] + data[:1]):
        line = p2 - p1
        if line == V(0, 0):
            continue
        direction = get_direction(line)
        if direction in "DU":
            y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)
            vertical_points.append((V(x=p1.x, y=y_min + 1), V(x=p1.x, y=y_max - 1)))
        elif direction in "LR":
            x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
            horizontal_points.append((V(x=x_min + 1, y=p1.y), V(x=x_max - 1, y=p1.y)))
    return vertical_points, horizontal_points


def data_points_from_rect(rect: Rectangle) -> list[V]:
    p1, p3 = rect
    p2 = V(p1.x, p3.y)
    p4 = V(p3.x, p1.y)
    return [p1, p2, p3, p4]


def get_outside_rectangles(data: list[V]) -> list[Rectangle]:
    outside_directions = {"DR", "LD", "UL", "RU"}
    outside_rectangles = []
    for p1, p2, p3 in zip(data, data[1:] + data[:1], data[2:] + data[:2]):
        direction = corner_direction(p1, p2, p3)
        if direction in outside_directions:
            outside_rectangles.append((p1, p3))
    return outside_rectangles


def edges_intersect(v_edge: Edge, h_edge: Edge) -> bool:
    min_v, max_v = (min(e.y for e in v_edge), max(e.y for e in v_edge))
    min_h, max_h = (min(e.x for e in h_edge), max(e.x for e in h_edge))
    v_aligned = min_v <= h_edge[0].y <= max_v
    h_aligned = min_h <= v_edge[0].x <= max_h
    return h_aligned and v_aligned


def part2(data: list[V]):
    """Solve part 2."""
    highest_area = 0
    outside_points = get_outside_points(data)
    # outside_rectangles = get_outside_rectangles(data)

    shape_v_edges, shape_h_edges = get_edges(data)

    for rect in itertools.combinations(data, 2):
        area = (rect[1] - rect[0]).area
        if area <= highest_area:
            continue
        if any(
            point_in_rectangle(outside_point, rect) for outside_point in outside_points
        ):
            continue
        full_rect = data_points_from_rect(rect)
        rect_v_edges, rect_h_edges = get_edges(full_rect)
        for rect_v_edge in rect_v_edges:
            if any(edges_intersect(rect_v_edge, h_edge) for h_edge in shape_h_edges):
                break
            else:
                for rect_h_edge in rect_h_edges:
                    if any(
                        edges_intersect(v_edge, rect_h_edge) for v_edge in shape_v_edges
                    ):
                        break
                    else:
                        highest_area = area
                    if area == 92:
                        breakpoint()
    return highest_area


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
