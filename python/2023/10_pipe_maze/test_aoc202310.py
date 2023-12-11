"""Tests for AoC 10, 2023: Pipe maze."""

# Third party imports
import aoc202310
import pytest


@pytest.fixture
def example1():
    puzzle_input = aoc202310.read_file("example1.txt")
    return aoc202310.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = aoc202310.read_file("example2.txt")
    return aoc202310.parse(puzzle_input)


@pytest.fixture
def example3():
    puzzle_input = aoc202310.read_file("example3.txt")
    return aoc202310.parse(puzzle_input)


@pytest.fixture
def example4():
    puzzle_input = aoc202310.read_file("example4.txt")
    return aoc202310.parse(puzzle_input)


@pytest.fixture
def real_data():
    puzzle_input = aoc202310.read_file("input.txt")
    return aoc202310.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...


# @pytest.mark.skip(reason="Not implemented")
def test_part1_example3(example3):
    """Test part 1 on example input."""
    assert aoc202310.part1(example3) == 8


# @pytest.mark.skip(reason="Not implemented")
def test_part2_example4(example4):
    """Test part 2 on example input."""
    assert aoc202310.part2(example4) == 8


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202310.part2(example2) == ...


# @pytest.mark.skip(reason="Not implemented")
def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202310.part1(real_data) == 6979


@pytest.mark.skip(reason="Not implemented")
def test_part2_real(real_data):
    """Test part 2 on real input."""
    assert aoc202310.part2(real_data) == ...
