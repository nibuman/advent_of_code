"""AoC 10, 2025: Factory."""

# Standard library imports
import enum
import pathlib
import sys
from datetime import datetime
from dataclasses import dataclass
import re
import itertools
from typing import Iterable


@dataclass
class Machine:
    light_positions: int
    switches_positions: list[int]
    jolts: list[int]

    @classmethod
    def from_row(cls, row: str) -> Machine:
        pattern = re.compile(
            pattern=r"\[(?P<lights>[\.#]+)\] (?P<switches>\([\(\) \d\,]+) {(?P<jolts>[\d\,]+)}"
        )
        row_match = re.match(pattern, row)
        assert row_match
        lights = Machine.parse_lights(row_match.group("lights"))
        switches_positions = Machine.parse_switches(row_match.group("switches"))
        jolts = [int(c) for c in row_match.group("jolts").split(",")]
        return Machine(
            light_positions=lights, switches_positions=switches_positions, jolts=jolts
        )

    @staticmethod
    def parse_lights(lights: str) -> int:
        return sum(1 << i for i, char in enumerate(lights) if char == "#")

    @staticmethod
    def parse_switches(switches: str) -> list[int]:
        switch_positions = []
        for switch in switches.split(" "):
            switch = switch.removeprefix("(").removesuffix(")")
            switch_positions.append(sum(1 << int(pos) for pos in switch.split(",")))
        return switch_positions


def parse(puzzle_input: str) -> list[Machine]:
    """Parse input."""
    return [Machine.from_row(row) for row in puzzle_input.split("\n")]


def part1(machines: list[Machine]):
    """Solve part 1."""
    switch_presses = []
    for machine in machines:
        for total_presses in range(len(machine.switches_positions) + 1):
            presses = itertools.combinations(machine.switches_positions, total_presses)
            # breakpoint()
            if any(
                press_switches(press) == machine.light_positions for press in presses
            ):
                switch_presses.append(total_presses)
                break
    return sum(switch_presses)


def press_switches(presses: Iterable[int]) -> int:
    lights = 0
    for press in presses:
        lights ^= press
    return lights


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
