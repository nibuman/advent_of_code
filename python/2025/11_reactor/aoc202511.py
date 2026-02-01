"""AoC 11, 2025: Reactor."""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass
from datetime import datetime

NetworkMap = dict[str, list[str]]


def parse(puzzle_input: str) -> NetworkMap:
    """Parse input."""
    data = puzzle_input.split("\n")
    data_map = {}
    for row in data:
        node, attached = row.split(":")
        data_map[node] = attached.strip().split(" ")
    return data_map


def count_route(
    device: str, input_data: NetworkMap, completed_paths: dict[str, int]
) -> int:
    if device in completed_paths:
        return completed_paths[device]
    route_count = 0
    for output in input_data[device]:
        if output == "out":
            completed_paths[device] = 1
            return 1
        route_count += count_route(
            device=output, input_data=input_data, completed_paths=completed_paths
        )
    completed_paths[device] = route_count
    return route_count


def part1(data):
    """Solve part 1."""
    return count_route(device="you", input_data=data, completed_paths={})


@dataclass(frozen=True, eq=True)
class Route:
    device: str
    fft: bool
    dac: bool


def count_route2(
    device: str,
    input_data: NetworkMap,
    completed_paths: dict[Route, int],
    dac: bool = False,
    fft: bool = False,
) -> int:
    if Route(device, fft, dac) in completed_paths:
        return completed_paths[Route(device, fft, dac)]
    route_count = 0
    dac = dac or (device == "dac")
    fft = fft or (device == "fft")
    for output in input_data[device]:
        if output == "out":
            completed_paths[Route(device, fft, dac)] = dac and fft
            return dac and fft
        route_count += count_route2(
            device=output,
            input_data=input_data,
            completed_paths=completed_paths,
            dac=dac,
            fft=fft,
        )
    completed_paths[Route(device, fft, dac)] = route_count
    return route_count


def part2(data):
    """Solve part 2."""
    return count_route2(device="svr", input_data=data, completed_paths={})


def solve(puzzle_input, input_name):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    for name, func in (("Part1", part1), ("Part2", part2)):
        if name == "Part1" and input_name == "example2.txt":
            continue
        if name == "Part2" and input_name == "example1.txt":
            continue
        # if name == "Part2" and input_name == "input.txt":
        #     continue
        t1 = datetime.now()
        result = func(data)
        t2 = datetime.now()
        yield name, result, (t2 - t1).microseconds


def read_file(file_name) -> str:
    PUZZLE_DIR = pathlib.Path(__file__).parent
    return pathlib.Path(PUZZLE_DIR / file_name).read_text().rstrip()


if __name__ == "__main__":
    DEFAULT_INPUT_FILES = ["example1.txt", "example2.txt", "input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(puzzle_input=read_file(file_name), input_name=file_name)
        print(
            "\n".join(
                f"{puzzle}: {solution} (in {time / 1000} ms)"
                for puzzle, solution, time in solutions
            )
        )
