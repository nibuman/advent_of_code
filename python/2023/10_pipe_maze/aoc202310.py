"""AoC 10, 2023: Pipe maze."""

# Standard library imports
import pathlib
import sys
from collections import deque
from itertools import product

N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)
COMPASS_POINTS = [N, S, E, W]
PIPES = {"|": [N, S], "-": [E, W], "L": [N, E], "J": [N, W], "7": [S, W], "F": [S, E]}


def parse(puzzle_input):
    """Parse input."""
    return [list(line) for line in puzzle_input]


def part1(data):
    """Solve part 1."""
    return follow_pipe(data)[1]


def get_start_directions(data, start_pos):
    next_positions = []
    for offset in COMPASS_POINTS:
        pos = position_add(start_pos, offset)
        try:
            neighbour_pos = get_positions(data, pos)
        except KeyError:
            continue
        if neighbour_pos:
            pos1, pos2 = neighbour_pos
            if (pos1 == start_pos) or (pos2 == start_pos):
                next_positions.append(pos)
    return next_positions


def follow_pipe(data):
    """Breadth-first search"""
    start_pos = get_start_pos(data)
    next_positions = get_start_directions(data, start_pos)
    counter = 0
    visited_positions = {start_pos}
    to_visit = deque(next_positions)
    new_positions = deque()
    paths_not_met = True
    while paths_not_met:
        counter += 1
        for visit_pos in to_visit:
            visited_positions.add(visit_pos)
            pos1, pos2 = get_positions(data, visit_pos)
            if (pos1 in visited_positions) and (pos2 in visited_positions):
                paths_not_met = False
                break
            elif pos1 in visited_positions:
                new_positions.append(pos2)
            else:
                new_positions.append(pos1)
        to_visit = new_positions
        new_positions = deque()
    return start_pos, counter, visited_positions


def position_add(point1, point2):
    return (point1[0] + point2[0], point1[1] + point2[1])


def position_sub(point1, point2):
    return (point1[0] - point2[0], point1[1] - point2[1])


def get_positions(data, point):
    r, c = point
    pipe_type = data[r][c]
    offsets = PIPES[pipe_type]
    return position_add(point, offsets[0]), position_add(point, offsets[1])


def part2(data):
    """Solve part 2.

    Works across each row looking at how many times the pipe is crossed.
    If it is crossed an odd number of times then must be inside the loop, if even then outside
    """
    start_pos, _, pipe_positions = follow_pipe(data)
    ALL_POSITIONS = set(product(range(len(data)), range(len(data[0]))))
    non_pipe_positions = ALL_POSITIONS - set(pipe_positions)
    fill_positions(data, non_pipe_positions, ".")
    data[start_pos[0]][start_pos[1]] = get_start_char(data, start_pos)
    for r, row in enumerate(data):
        counter = 0
        previous_directions = set()
        for c, char in enumerate(row):
            if char == ".":
                data[r][c] = str(counter % 2)
                previous_directions = set()
            elif char in ("-"):
                continue
            else:
                directions = get_vertical_directions(data, (r, c)) | previous_directions
                if directions == {N, S}:
                    counter += 1
                    previous_directions = set()
                elif previous_directions:
                    previous_directions = set()
                else:
                    previous_directions = get_vertical_directions(data, (r, c))
    return sum(char == "1" for row in data for char in row)


def get_start_char(data, pos):
    neighbour1, neighbour2 = get_start_directions(data, pos)
    offset1 = position_sub(neighbour1, pos)
    offset2 = position_sub(neighbour2, pos)
    directions = {offset1, offset2}
    for char, pipe_dirs in PIPES.items():
        if directions == set(pipe_dirs):
            return char


def get_directions(data, pos):
    r, c = pos
    char = data[r][c]
    return set(PIPES[char])


def get_vertical_directions(data, pos):
    return get_directions(data, pos) - {E, W}


def fill_positions(data, positions, char):
    for pos in positions:
        data[pos[0]][pos[1]] = char


def get_start_pos(data):
    return [
        (r, c)
        for r, row in enumerate(data)
        for c, char in enumerate(row)
        if char == "S"
    ][0]


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    yield "Part 1", part1(data)
    yield "Part 2", part2(data)


def read_file(file_name):
    PUZZLE_DIR = pathlib.Path(__file__).parent
    return pathlib.Path(PUZZLE_DIR / file_name).read_text().rstrip().split("\n")


if __name__ == "__main__":
    DEFAULT_INPUT_FILES = ["input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(puzzle_input=read_file(file_name))
        print("\n".join(f"{puzzle}: {solution}" for puzzle, solution in solutions))
