"""AoC 5, 2025: Cafeteria."""

# Standard library imports
from dataclasses import dataclass
import pathlib
import sys
from collections import deque


@dataclass
class Range:
    start: int
    end: int

    @property
    def id_count(self):
        return self.end - self.start + 1

    @classmethod
    def from_string(cls, puzzle_input: str):
        start, end = puzzle_input.split("-")
        return cls(start=int(start), end=int(end))

    def __contains__(self, item: int) -> bool:
        return item in range(self.start, self.end + 1)


def parse(puzzle_input: str) -> tuple[list[Range], list[int]]:
    """Parse input."""
    range_data, ingredient_ID_data = puzzle_input.split("\n\n")
    ranges: list[Range] = [Range.from_string(r) for r in range_data.split("\n")]
    ingredient_IDs = [int(i) for i in ingredient_ID_data.split("\n")]
    return ranges, ingredient_IDs


def part1(data: tuple[list[Range], list[int]]) -> int:
    """Solve part 1."""
    ranges, ingredient_IDs = data
    count = 0
    for ingredient_ID in ingredient_IDs:
        for ID_range in ranges:
            if ingredient_ID in ID_range:
                count += 1
                break
    return count


def rationalise_ranges(ranges: list[Range]) -> list[Range]:
    range_deque = deque(sorted(ranges, key=lambda x: x.start))
    new_ranges: list[Range] = []
    first_range = range_deque.popleft()
    while range_deque:
        second_range = range_deque.popleft()
        if second_range.start > first_range.end:
            new_ranges.append(first_range)
            first_range = second_range
        elif second_range.end > first_range.end:
            first_range.end = second_range.end
    new_ranges.append(Range(start=first_range.start, end=first_range.end))
    return new_ranges


def part2(data):
    """Solve part 2."""
    ranges, _ = data
    new_ranges = rationalise_ranges(ranges)
    return sum(r.id_count for r in new_ranges)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    yield "Part 1", part1(data)
    yield "Part 2", part2(data)


def read_file(file_name) -> str:
    PUZZLE_DIR = pathlib.Path(__file__).parent
    return pathlib.Path(PUZZLE_DIR / file_name).read_text().rstrip()


if __name__ == "__main__":
    DEFAULT_INPUT_FILES = ["example1.txt", "input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(puzzle_input=read_file(file_name))
        print("\n".join(f"{puzzle}: {solution}" for puzzle, solution in solutions))
