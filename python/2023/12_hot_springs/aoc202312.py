"""AoC 12, 2023: Hot springss."""

# Standard library imports
import pathlib
import sys
from itertools import permutations
from dataclasses import dataclass


@dataclass()
class Record:
    springs: list[str]
    groups: list[int]


def parse(puzzle_input):
    """Parse input."""
    records = []
    for line in puzzle_input:
        spring_map, groups = line.split()
        records.append(
            Record(
                springs=list(spring_map), groups=[int(num) for num in groups.split(",")]
            )
        )
    return records


def part1(data: list[Record]):
    """Solve part 1."""
    counts = []
    for idx, record in enumerate(data):
        unknowns = record.springs.count("?")
        knowns = record.springs.count("#")
        total = sum(record.groups)
        additional_required = total - knowns
        perm_string = ("#" * additional_required) + (
            "." * (unknowns - additional_required)
        )
        perms = set(permutations(perm_string, unknowns))
        unknown_positions = [
            idx for idx, char in enumerate(record.springs) if char == "?"
        ]
        print(f"{idx} / {len(data)} ({len(perms)})")
        valid_count = 0
        for perm in perms:
            for idx, char in zip(unknown_positions, perm):
                record.springs[idx] = char
            if valid_record(record=record):
                valid_count += 1
        counts.append(valid_count)
    print(counts)
    return sum(counts)


def valid_record(record: Record) -> bool:
    actual_groups = [
        len(spring) for spring in "".join(record.springs).split(".") if spring
    ]
    return all(
        actual == expected for actual, expected in zip(actual_groups, record.groups)
    )


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
    DEFAULT_INPUT_FILES = ["example2.txt", "input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(puzzle_input=read_file(file_name))
        print("\n".join(f"{puzzle}: {solution}" for puzzle, solution in solutions))
