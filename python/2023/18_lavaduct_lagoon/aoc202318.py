"""AoC 18, 2023: Lavaduct lagoon."""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass
from utils.vectors import Vector as V
from utils.vectors import shoelace

#  Direction vectors
U = V(-1, 0)
D = V(1, 0)
L = V(0, -1)
R = V(0, 1)


@dataclass
class Instruction:
    vector: V
    colour: str


def parse(puzzle_input) -> list[Instruction]:
    """Parse input."""
    direction_map = {"U": U, "D": D, "L": L, "R": R}
    instructions = []
    for line in puzzle_input:
        line_data = line.split()
        direction = direction_map[line_data[0]]
        distance = int(line_data[1])
        vector = direction * distance
        colour = line_data[2].removeprefix("(").removesuffix(")")
        instructions.append(Instruction(vector, colour))
    return instructions


def part1(data: list[Instruction]):
    """Solve part 1."""
    return calc_area(data)


def calc_area(data) -> int:
    coordinates = [V(0, 0)]
    for line in data:
        coordinates.append(coordinates[-1] + line.vector)
    interior_points = shoelace(
        coordinates[1:]
    )  #  Shoelace formula to area inside point co-ordinates
    perimeter = sum(abs(ins.vector.row) + abs(ins.vector.col) for ins in data)
    # Need to account for the thickness of the perimeter line
    return int(f"{interior_points + (perimeter/2) + 1:.0f}")


def part2(data: list[Instruction]):
    """Solve part 2."""
    coordinates = [
        Instruction(vector=parse_hex(ins.colour), colour=ins.colour) for ins in data
    ]
    return calc_area(coordinates)


def parse_hex(colour: str) -> V:
    hex_distance = colour[1:6]
    hex_direction = colour[-1]
    direction_map = {"0": R, "1": D, "2": L, "3": U}
    return direction_map[hex_direction] * int(hex_distance, 16)


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
