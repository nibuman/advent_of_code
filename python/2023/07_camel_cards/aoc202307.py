"""AoC 7, 2023: Camel cards."""

# Standard library imports
import pathlib
import sys

from typing import NamedTuple
from collections import Counter


class Hand(NamedTuple):
    cards: str
    bid: int


def part1(hands):
    return sum(
        hand.bid * rank
        for rank, hand in enumerate(sorted(hands, key=hand_rank), start=1)
    )


def part2(hands):
    return sum(
        hand.bid * rank
        for rank, hand in enumerate(sorted(hands, key=hand_rank2), start=1)
    )


def parse(data):
    return [Hand(cards=line.split()[0], bid=int(line.split()[1])) for line in data]


def hand_rank(hand: Hand):
    trick_rank = get_trick_rank(hand=hand)
    subs = {"A": "E", "K": "D", "Q": "C", "J": "B", "T": "A"}
    sortable_hand = substitute_values(hand.cards, subs)
    return trick_rank + sortable_hand


def hand_rank2(hand: Hand):
    subs = {"A": "E", "K": "D", "Q": "C", "J": "0", "T": "A"}
    sortable_hand = substitute_values(hand.cards, subs)
    values = [str(n) for n in range(1, 10)] + list(subs.keys())
    if "J" in hand.cards:
        trick_rank = max(
            get_trick_rank(Hand(cards=hand.cards.replace("J", v), bid=0))
            for v in values
        )
    else:
        trick_rank = get_trick_rank(hand=hand)
    return trick_rank + sortable_hand


def substitute_values(cards, substitutes):
    for original, new in substitutes.items():
        cards = cards.replace(original, new)
    return cards


def get_trick_rank(hand):
    trick = Counter(str(n) for n in Counter(hand.cards).values())
    trick_rank = "1"
    if trick["5"]:
        trick_rank = "7"
    if trick["4"]:
        trick_rank = "6"
    elif trick["3"] and trick["2"]:
        trick_rank = "5"
    elif trick["3"]:
        trick_rank = "4"
    elif trick["2"] == 2:
        trick_rank = "3"
    elif trick["2"]:
        trick_rank = "2"
    return trick_rank

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
