"""Tests for AoC 7, 2025: Laboratories."""

# Third party imports
import aoc202507
import pytest


@pytest.fixture
def example1():
    puzzle_input = aoc202507.read_file("example1.txt")
    return aoc202507.parse(puzzle_input)


@pytest.fixture
def real_data():
    puzzle_input = aoc202507.read_file("input.txt")
    return aoc202507.parse(puzzle_input)


def test_parse_example1_start_position(example1):
    """Test that input is parsed properly."""
    start, *_ = example1
    assert start == (0, 7)


def test_parse_example1_splitters(example1):
    """Test that input is parsed properly."""
    _, splitters, *_ = example1
    assert len(splitters) == 22


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202507.part1(example1) == 21


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202507.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202507.part1(real_data) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_real(real_data):
    """Test part 2 on real input."""
    assert aoc202507.part2(real_data) == ...
