"""AoC 15, 2023: Lens library."""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    label: str
    hash_: int
    operator: str
    focal_length: int | None = None


@dataclass(frozen=True)
class Lens:
    label: str
    focal_length: int


def parse(puzzle_input):
    """Parse input."""
    return puzzle_input[0].split(",")


def part1(data):
    """Solve part 1."""
    return sum(get_hash(string) for string in data)


def get_hash(string):
    current_value = 0
    for char in string:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def part2(data):
    """Solve part 2."""
    instructions = get_instuctions(data)
    boxes: list[list[Lens]] = [[] for _ in range(256)]
    op = {"-": op_minus, "=": op_equals}
    for instruction in instructions:
        op[instruction.operator](
            box=boxes[instruction.hash_],
            label=instruction.label,
            focal_length=instruction.focal_length,
        )
    return focal_power(boxes)


def focal_power(boxes: list[list[Lens]]):
    scores = []
    for b, box in enumerate(boxes):
        for l, lens in enumerate(box):
            scores.append((b + 1) * (l + 1) * lens.focal_length)
    return sum(scores)


def op_minus(box: list[Lens], label, focal_length=None):
    for idx, lens in enumerate(box):
        if lens.label == label:
            box.pop(idx)
            return idx


def op_equals(box: list[Lens], label, focal_length):
    this_lens = Lens(label=label, focal_length=focal_length)
    pos = op_minus(box, label)
    if pos is None:
        box.append(this_lens)
    else:
        box.insert(pos, this_lens)


def get_instuctions(data) -> list[Instruction]:
    instructions = []
    for string in data:
        if "-" in string:
            label = string.removesuffix("-")
            instructions.append(
                Instruction(label=label, hash_=get_hash(label), operator="-")
            )
        else:
            label, lens = string.split("=")
            instructions.append(
                Instruction(
                    label=label,
                    hash_=get_hash(label),
                    operator="=",
                    focal_length=int(lens),
                )
            )
    return instructions


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
