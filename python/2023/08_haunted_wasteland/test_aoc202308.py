"""Tests for AoC 8, 2023: Haunted wasteland."""

# Third party imports
import aoc202308
import pytest


@pytest.fixture
def example1():
    puzzle_input = aoc202308.read_file("example1.txt")
    return aoc202308.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = aoc202308.read_file("example2.txt")
    return aoc202308.parse_data(puzzle_input)


# @pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    directions, dir_map = example1
    assert directions == "RL"
    assert dir_map["AAA"] == ("BBB", "CCC")


# @pytest.mark.skip(reason="Not implemented")
def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202308.part1(example1) == 2


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202308.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202308.part2(example2) == ...
