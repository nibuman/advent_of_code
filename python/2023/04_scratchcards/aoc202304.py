"""AoC 4, 2023: Scratchcards."""

# Standard library imports
import pathlib
import sys
from collections import deque
from functools import lru_cache


def part1(cards):
    return sum(2 ** (nums - 1) for nums in cards.values() if nums > 0)


def part2(cards):
    card_stack = deque(cards.keys())
    card_count = 0
    while card_stack:
        card_id = card_stack.pop()
        for n in range(card_id + 1, card_id + cards[card_id] + 1):
            card_stack.appendleft(n)
        card_count += 1
    return card_count


def parse(data):
    """Mapping of cards to the number of winning numbers"""
    cards = {}
    for game in data:
        game_id, values = game.split(": ")
        winning_number_card, my_number_card = values.split(" | ")
        winning_numbers = set(int(n) for n in winning_number_card.split())
        my_numbers = set(int(n) for n in my_number_card.split())
        cards[int(game_id.removeprefix("Card "))] = len(my_numbers & winning_numbers)
    return cards


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
