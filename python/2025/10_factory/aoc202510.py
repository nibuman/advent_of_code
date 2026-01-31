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

import numpy as np
from scipy.optimize import LinearConstraint, milp

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


def get_linear_equations(machine: Machine) -> np.typing.ArrayLike:
    """Represent each linear equation as shown:
    s4 + s5 = 3 =>      [0, 0, 0, 0, 1, 1]
    s1 + s5 = 5 =>      [0, 1, 0, 0, 0, 1]
    s2 + s3 + s4 = 4 => [0, 0, 1, 1, 1, 0]
    s0 + s1 + s3 = 7 => [1, 1, 0, 1, 0, 0]
    Return as a matrix
    The results of the equation (3, 4, 5, and 7) will be supplied separately to the solver as upper/lower bounds for the equations
    """
    equation_count = len(machine.jolts)
    switch_count = len(machine.switches)
    equations = []
    for eq_id in range(equation_count):
        this_equation = [0] * switch_count
        for s_id, switch in enumerate(machine.switches):
            if eq_id in switch:
                this_equation[s_id] = 1
        equations.append(this_equation)
    return np.array(equations)


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
    """For example1 row1: (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    Adding the number of presses for each switch s:
    s4 + s5 = 3
    s1 + s5 = 5
    s2 + s3 + s4 = 4
    s0 + s1 + s3 = 7
    while trying to minimise s0 + s1 + s2 + s3 + s4 + s5 ([1, 1, 1, 1, 1])
    """
    # Trying to minimise this, the coeffs for each switch
    c = np.array([1] * len(machine.switches))

    # Matrix, each row is an equation, each col a switch
    A = get_linear_equations(machine=machine)

    # The upper and lower bounds. Using equality (rather than >, < inequalities) so they're the same
    b_l = b_u = np.array(machine.jolts)
    constraints = LinearConstraint(A, b_l, b_u)

    # Indicates (with a '1') which coefficients should be integral (all of them!)
    integrality = np.ones_like(c)

    res = milp(c=c, constraints=constraints, integrality=integrality)
    return int(sum(res.x))


def part2(data: list[Machine]):
    """Solve part 2."""
    return sum(presses_required(machine) for machine in data)


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
            ),
            flush=True,
        )
