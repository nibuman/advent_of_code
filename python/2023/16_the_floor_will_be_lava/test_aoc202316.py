"""Tests for AoC 16, 2023: The floor will be lava."""

# Third party imports
import aoc202316
import pytest


@pytest.fixture
def example1():
    puzzle_input = aoc202316.read_file("example1.txt")
    return aoc202316.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = aoc202316.read_file("example2.txt")
    return aoc202316.parse(puzzle_input)


@pytest.fixture
def real_data():
    puzzle_input = aoc202316.read_file("input.txt")
    return aoc202316.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...


# @pytest.mark.skip(reason="Not implemented")
def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202316.part1(example1) == 46


# @pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202316.part2(example1) == 51


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202316.part2(example2) == ...


# @pytest.mark.skip(reason="Not implemented")
def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202316.part1(real_data) == 7498


# @pytest.mark.skip(reason="Not implemented")
def test_part2_real(real_data):
    """Test part 2 on real input."""
    assert aoc202316.part2(real_data) == 7846
