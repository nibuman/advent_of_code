"""Tests for AoC 10, 2025: Factory."""

# Third party imports
import aoc202510
import pytest


@pytest.fixture
def example1():
    puzzle_input = aoc202510.read_file("example1.txt")
    return aoc202510.parse(puzzle_input)


@pytest.fixture
def real_data():
    puzzle_input = aoc202510.read_file("input.txt")
    return aoc202510.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...


@pytest.mark.skip(reason="Not implemented")
def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202510.part1(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202510.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202510.part1(real_data) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_real(real_data):
    """Test part 2 on real input."""
    assert aoc202510.part2(real_data) == ...
