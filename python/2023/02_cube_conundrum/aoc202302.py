"""AoC 2, 2023: Cube conundrum."""

# Standard library imports
import pathlib
import sys


def part1(data):
    limits = dict(red=12, green=13, blue=14)
    possibles = []
    for game in data:
        possible = True
        game_id, sets = game.split(": ")
        for set_ in sets.split("; "):
            for cube in set_.split(", "):
                number, colour = cube.split()
                if int(number) > limits[colour]:
                    possible = False
                    break
            if not possible:
                break
        if possible:
            possibles.append(int(game_id.removeprefix("Game ")))
    return sum(possibles)


def part2(data):
    products = []
    for game in data:
        cubes = dict(red=[], green=[], blue=[])
        game_id, sets = game.split(": ")
        for set_ in sets.split("; "):
            for cube in set_.split(", "):
                number, colour = cube.split()
                cubes[colour].append(int(number))
        minimum_cubes = [
            max(v) for v in cubes.values()
        ]  # The minimum number of cubes is the max that was drawn of each colour
        products.append(minimum_cubes[0] * minimum_cubes[1] * minimum_cubes[2])
    return sum(products)


def parse(data):
    return data


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
