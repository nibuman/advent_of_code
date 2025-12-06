"""Tests for AoC 5, 2025: Cafeteria."""

# Third party imports
import aoc202505
import pytest


@pytest.fixture
def example1():
    puzzle_input = aoc202505.read_file("example1.txt")
    return aoc202505.parse(puzzle_input)


@pytest.fixture
def real_data():
    puzzle_input = aoc202505.read_file("input.txt")
    return aoc202505.parse(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    expected_ranges = [
        aoc202505.Range(start=3, end=5),
        aoc202505.Range(start=10, end=14),
        aoc202505.Range(start=16, end=20),
        aoc202505.Range(start=12, end=18),
    ]
    expected_IDs = [
        1,
        5,
        8,
        11,
        17,
        32,
    ]
    ranges, ingredient_IDs = example1
    assert expected_ranges == ranges
    assert expected_IDs == ingredient_IDs


def test_rationalise_ranges(example1):
    expected_ranges = [
        aoc202505.Range(start=3, end=5),
        aoc202505.Range(start=10, end=20),
    ]
    ranges, _ = example1
    assert expected_ranges == aoc202505.rationalise_ranges(ranges)


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202505.part1(example1) == 3


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202505.part2(example1) == 14


def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202505.part1(real_data) == 558


def test_part2_real(real_data):
    """Test part 2 on real input."""
    assert aoc202505.part2(real_data) == 344813017450467
