"""AoC 1, 2025: Secret Entrance."""

# Standard library imports
import pathlib
import sys
import operator
from typing import Generator
START_POS = 50
FUNC_MAP = {"L": operator.sub, "R": operator.add}

def parse(puzzle_input):
    """Parse input."""
    return puzzle_input

def rotations(data) -> Generator[tuple[str, int]]:    
    for d in data:
        direction = d[0]
        distance = int(d[1:])
        yield direction, distance

def part1(data):
    positions = [START_POS,]    
    for direction, distance in rotations(data):
        pos = FUNC_MAP[direction](positions[-1], distance) % 100
        positions.append(pos)
    return sum(p==0 for p in positions)


def part2(data):
    """Solve part 2."""
    counts = 0
    pos = START_POS
    for direction, distance in rotations(data):
        if distance == 0:
            continue
        shift = FUNC_MAP[direction](pos, distance) 
        if (pos != 0) and (shift >= 100):
            counts += shift // 100
        elif (pos !=0) and (shift <= 0):
            counts += abs((shift-1)//100)
        elif pos == 0:
            counts += distance // 100
        pos = shift % 100
    return counts             


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
