"""AoC 5, 2023: If you give a seed a fertiliser."""

# Standard library imports
import pathlib
import sys
from typing import NamedTuple


class Ranges(NamedTuple):
    destination_start: int
    start: int
    range_length: int
    end: int = 0


def part1(data: tuple[list[int], dict[str, list[Ranges]]]):
    locations = []
    seeds, source = data
    for seed in seeds:
        locations.append(get_location(seed, source))
    return min(locations)


def part2(data: tuple[list[int], dict[str, list[Ranges]]]):
    locations = []
    seeds, source = data
    new_seeds = []
    for start, range_ in zip(seeds[::2], seeds[1::2]):
        new_seeds.append(
            Ranges(
                destination_start=0,
                start=start,
                range_length=range_,
                end=start + range_ - 1,
            )
        )
    locations = get_location2(new_seeds, source)
    return min(loc.start for loc in locations)


def get_location2(seeds: list[Ranges], source: dict[str, list[Ranges]]):
    source_stack = seeds
    destination_stack = []
    for s in source:
        while source_stack:
            current_seeds = source_stack.pop()
            for range_ in source[s]:
                range_end = range_.start + range_.range_length - 1
                if (current_seeds.start < range_.start) and (
                    current_seeds.end > range_.start
                ):
                    source_stack.append(
                        Ranges(
                            destination_start=0,
                            start=current_seeds.start,
                            range_length=0,
                            end=range_.start - 1,
                        )
                    )
                    current_seeds = Ranges(
                        destination_start=0,
                        start=range_.start,
                        range_length=0,
                        end=current_seeds.end,
                    )
                if (current_seeds.end > range_end) and (
                    current_seeds.start < range_end
                ):
                    source_stack.append(
                        Ranges(
                            destination_start=0,
                            start=range_end + 1,
                            range_length=0,
                            end=current_seeds.end,
                        )
                    )
                    current_seeds = Ranges(
                        destination_start=0,
                        start=current_seeds.start,
                        range_length=0,
                        end=range_end,
                    )
                if (current_seeds.start >= range_.start) and (
                    current_seeds.end <= range_end
                ):
                    offset = current_seeds.start - range_.start
                    destination_stack.append(
                        Ranges(
                            destination_start=0,
                            start=range_.destination_start + offset,
                            range_length=0,
                            end=range_.destination_start
                            + offset
                            + (current_seeds.end - current_seeds.start),
                        )
                    )
                    break
            else:
                destination_stack.append(
                    Ranges(
                        destination_start=0,
                        start=current_seeds.start,
                        range_length=0,
                        end=current_seeds.end,
                    )
                )

        source_stack = destination_stack
        destination_stack = []
    return source_stack


def get_location(seed, source: dict[str, list[Ranges]]):
    current_num = seed
    for s in source:
        for range_ in source[s]:
            offset = current_num - range_.start
            if offset < 0:
                continue
            elif current_num >= range_.start + range_.range_length:
                continue
            else:
                current_num = range_.destination_start + offset
                break
    return current_num


def parse(data) -> tuple[list[int], dict[str, list[Ranges]]]:
    seeds = []
    source = {}
    for line in data:
        if "seeds: " in line:
            seeds.extend(int(num) for num in line.removeprefix("seeds: ").split())
            continue
        elif not line:
            continue
        elif "map" in line:
            key = line.split("-")[0]
            source[key] = []
        else:
            source[key].append(Ranges(*[int(n) for n in line.split()]))
    return seeds, source


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
