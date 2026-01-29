"""AoC 10, 2025: Factory."""

# Standard library imports
import collections
import itertools
import pathlib
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from operator import xor
from typing import Iterable

PATTERN = re.compile(
    r"\[(?P<lights>[\.#]+)\] (?P<switches>\([\(\) \d\,]+) {(?P<jolts>[\d\,]+)}"
)

type Switch = tuple[int, ...]


@dataclass
class Machine:
    light_positions: int
    switches_positions: list[int]
    jolts: list[int]
    switches: list[Switch]

    @classmethod
    def from_row(cls, row: str) -> Machine:
        row_match = re.match(PATTERN, row)
        assert row_match
        lights = Machine.parse_lights(row_match.group("lights"))
        switches_positions, switches = Machine.parse_switches(
            row_match.group("switches")
        )
        jolts = [int(c) for c in row_match.group("jolts").split(",")]
        return Machine(
            light_positions=lights,
            switches_positions=switches_positions,
            jolts=jolts,
            switches=switches,
        )

    @staticmethod
    def parse_lights(lights: str) -> int:
        return sum(1 << i for i, char in enumerate(lights) if char == "#")

    @staticmethod
    def parse_switches(switches: str) -> tuple[list[int], list[tuple[int, ...]]]:
        switch_positions = []
        switches_ = []
        for switch in switches.split(" "):
            switch = switch.removeprefix("(").removesuffix(")")
            switches_.append(tuple(int(x) for x in switch.split(",")))
            switch_positions.append(sum(1 << int(pos) for pos in switch.split(",")))
        return switch_positions, switches_


def press_switches(presses: Iterable[int]) -> int:
    return reduce(xor, presses, initial=0)


def calc_joltages(presses: Iterable[tuple[int, ...]], jolt_count: int) -> list[int]:
    joltages = collections.Counter(itertools.chain(*presses))
    return [joltages[i] for i in range(jolt_count)]


def parse(puzzle_input: str) -> list[Machine]:
    """Parse input."""
    return [Machine.from_row(row) for row in puzzle_input.split("\n")]


def part1(machines: list[Machine]):
    """Solve part 1."""
    switch_presses = []
    for machine in machines:
        for total_presses in range(len(machine.switches_positions) + 1):
            presses = itertools.combinations(machine.switches_positions, total_presses)
            if any(
                press_switches(press) == machine.light_positions for press in presses
            ):
                switch_presses.append(total_presses)
                break
    return sum(switch_presses)


def presses_required(machine: Machine) -> int:
    available_switches = [s for s in machine.switches if s[0] == 0]
    current_sequences = list(
        itertools.combinations_with_replacement(available_switches, machine.jolts[0])
    )
    for num, jolts in enumerate(machine.jolts[1:], start=1):
        new_sequences = []
        available_switches = [s for s in machine.switches if s[0] == num]
        for sequence in current_sequences:
            existing_jolts = calc_joltages(sequence, len(machine.jolts))[num]
            if existing_jolts > jolts:
                continue

            switch_combinations = list(
                itertools.combinations_with_replacement(
                    available_switches, jolts - existing_jolts
                )
            )
            for comb in switch_combinations:
                new_sequences.append([*itertools.chain(sequence, comb)])
        breakpoint()
        current_sequences = new_sequences
        print(f"{len(current_sequences)=}")
        new_sequences = []
    return min(len(s) for s in current_sequences)


def part2(data: list[Machine]):
    """Solve part 2."""
    return sum(presses_required(machine) for machine in data)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    for name, func in (("Part1", part1), ("Part2", part2)):
        t1 = datetime.now()
        result = func(data[:2])
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
            ),
            flush=True,
        )
