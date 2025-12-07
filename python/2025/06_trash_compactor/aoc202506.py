"""AoC 6, 2025: Trash Compactor."""

# Standard library imports
from dataclasses import dataclass
import pathlib
import sys
from typing import Sequence, Callable
import math


@dataclass
class MathProblem:
    nums: list[int]
    operator: str

    @classmethod
    def from_seq_of_str(cls, col: Sequence[str]) -> MathProblem:
        """Expects a math problem in the format ["num1", "num2", ..., "op"]"""
        *nums, op = col
        return cls(nums=[int(n) for n in nums], operator=op)

    @property
    def _func(self) -> Callable[[Sequence], int]:
        fn_map = {"*": math.prod, "+": sum}
        return fn_map[self.operator]

    def compute(self) -> int:
        return self._func(self.nums)


def parse(puzzle_input: str) -> list[str]:
    """Parse input."""
    by_rows = puzzle_input.split("\n")
    return by_rows


def part1(data):
    """Solve part 1."""
    by_rows = [[s for s in row.split(" ") if s] for row in data]
    by_cols = [MathProblem.from_seq_of_str(col) for col in zip(*by_rows)]
    return sum(mp.compute() for mp in by_cols)


def part2(data_by_rows):
    """Solve part 2."""
    problems = []
    by_cols = zip(*data_by_rows)
    op = ""
    nums = []
    for col in by_cols:
        *digits, _op = col
        num = "".join(digits).strip()
        if not num:
            problems.append(MathProblem.from_seq_of_str([*nums, op]))
            nums = []
            op = ""
        else:
            nums.append(num)
            op = _op.strip() or op
    problems.append(MathProblem.from_seq_of_str([*nums, op]))  # breakpoint()
    return sum(mp.compute() for mp in problems)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    yield "Part 1", part1(data)
    yield "Part 2", part2(data)


def read_file(file_name) -> str:
    PUZZLE_DIR = pathlib.Path(__file__).parent
    return pathlib.Path(PUZZLE_DIR / file_name).read_text()


if __name__ == "__main__":
    DEFAULT_INPUT_FILES = ["example1.txt", "input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(puzzle_input=read_file(file_name))
        print("\n".join(f"{puzzle}: {solution}" for puzzle, solution in solutions))
