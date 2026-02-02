"""AoC 12, 2025: Christmas Tree Farm."""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass
from datetime import datetime

Shape = list[list[int]]


@dataclass(frozen=True, eq=True)
class Region:
    w: int
    d: int
    quantities: list[int]

    @property
    def area(self):
        return self.w * self.d

    @classmethod
    def from_string(cls, input_str) -> Region:
        region, qs = input_str.split(": ")
        w, d = [int(n) for n in region.split("x")]
        quantities = [int(n) for n in qs.split(" ")]
        return Region(w=w, d=d, quantities=quantities)


def filled_area(shape: Shape) -> int:
    return sum(sum(r) for r in shape)


def parse_shape(shape_data: str) -> Shape:
    shape: Shape = []
    for line in shape_data.split()[1:]:
        bool_line = line.replace(".", "0").replace("#", "1")
        shape.append([int(b) for b in bool_line])
    return shape


def parse(puzzle_input: str) -> tuple[list[Shape], list[Region]]:
    """Parse input."""
    parts = puzzle_input.split("\n\n")
    shapes = [parse_shape(part) for part in parts[:-1]]
    regions = [Region.from_string(line) for line in (parts[-1:][0]).split("\n")]
    return shapes, regions


def part1(shapes: list[Shape], regions: list[Region]) -> int:
    """Solve part 1."""
    count = 0
    for region in regions:
        present_area = sum(
            filled_area(shape=shapes[i]) * count
            for i, count in enumerate(region.quantities)
        )
        if present_area <= region.area:
            count += 1
    return count


def part2(data):
    """Solve part 2."""


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    for name, func in (("Part1", part1),):  # ("Part2", part2)):
        t1 = datetime.now()
        result = func(*data)
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
