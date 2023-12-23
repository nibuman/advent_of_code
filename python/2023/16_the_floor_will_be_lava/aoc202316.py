"""AoC 16, 2023: The floor will be lava."""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass
from utils.vectors import Vector as V

# Direction vectors
N = V(-1, 0)
S = V(1, 0)
E = V(0, 1)
W = V(0, -1)

# Direction mappings (don't want to have to create these every time function is called)
BACKSLASH_VEC_MAP = {N: W, E: S, S: E, W: N}
FORWARDSLASH_VEC_MAP = {N: E, E: N, S: W, W: S}


@dataclass
class LightBeam:
    location: V
    direction: V

    def __hash__(self) -> int:
        return hash((*self.location, *self.direction))

    def __eq__(self, other) -> bool:
        return (self.location == other.location) and (self.direction == other.direction)


def parse(puzzle_input):
    """Parse input."""
    return puzzle_input


def part1(data):
    """Solve part 1."""
    return count_energised(data, initial_beam=LightBeam(location=V(0, 0), direction=E))


def part2(data):
    """Solve part 2."""
    start_beams = []
    for r in range(len(data)):
        start_beams.extend(
            [
                LightBeam(location=V(r, 0), direction=E),
                LightBeam(location=V(r, len(data[0]) - 1), direction=W),
            ]
        )
    for c in range(len(data[0])):
        start_beams.extend(
            (
                [
                    LightBeam(location=V(0, c), direction=S),
                    LightBeam(location=V(len(data) - 1, c), direction=N),
                ]
            )
        )
    return max(count_energised(data, initial_beam) for initial_beam in start_beams)


def count_energised(data, initial_beam) -> int:
    beams = [initial_beam]
    visited = set()
    while beams:
        beam = beams.pop()
        r, c = beam.location
        if any(
            (r < 0, r >= len(data), c < 0, c >= len(data[0]), beam in visited)
        ):  # Off edge of map or already visited
            continue
        char = data[r][c]
        visited.add(beam)
        beams.extend(FUNC_MAPPINGS[char](beam))
    return len(set(beam.location for beam in visited))


def print_visited(visited, data):
    for r in range(len(data)):
        row = []
        for c in range(len(data[0])):
            char = "."
            for d in (N, S, E, W):
                if LightBeam(location=V(r, c), direction=d) in visited:
                    char = "#"
            row.append(char)
        print("".join(row))


def backslash(beam: LightBeam) -> list[LightBeam]:
    direction = BACKSLASH_VEC_MAP[beam.direction]
    return [LightBeam(location=beam.location + direction, direction=direction)]


def forwardslash(beam: LightBeam) -> list[LightBeam]:
    direction = FORWARDSLASH_VEC_MAP[beam.direction]
    return [LightBeam(location=beam.location + direction, direction=direction)]


def dot(beam: LightBeam) -> list[LightBeam]:
    direction = beam.direction
    return [LightBeam(location=beam.location + direction, direction=direction)]


def pipe(beam: LightBeam) -> list[LightBeam]:
    if beam.direction in (N, S):
        return dot(beam)
    else:
        return [
            LightBeam(location=beam.location + direction, direction=direction)
            for direction in (N, S)
        ]


def dash(beam: LightBeam) -> list[LightBeam]:
    if beam.direction in (E, W):
        return dot(beam)
    else:
        return [
            LightBeam(location=beam.location + direction, direction=direction)
            for direction in (E, W)
        ]


FUNC_MAPPINGS = {
    "\\": backslash,
    ".": dot,
    "/": forwardslash,
    "|": pipe,
    "-": dash,
}


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
