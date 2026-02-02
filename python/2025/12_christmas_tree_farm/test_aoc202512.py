"""Tests for AoC 12, 2025: Christmas Tree Farm."""

# Third party imports
import aoc202512
import pytest


@pytest.fixture
def example1():
    breakpoint()
    puzzle_input = aoc202512.read_file("example1.txt")
    return aoc202512.parse(puzzle_input)


@pytest.fixture
def real_data():
    puzzle_input = aoc202512.read_file("input.txt")
    return aoc202512.parse(puzzle_input)


def test_parse_shape():
    shape_data = """0:
###
##.
##."""
    expected_result = [[1, 1, 1], [1, 1, 0], [1, 1, 0]]
    result = aoc202512.parse_shape(shape_data)
    assert result == expected_result


def test_filled_area():
    shape = [[1, 0, 0], [1, 1, 0], [1, 1, 1]]
    expected_result = 6
    result = aoc202512.filled_area(shape=shape)
    assert result == expected_result


def test_Region_from_string():
    region_str = "12x5: 1 0 1 0 2 2"
    expected_result = aoc202512.Region(w=12, d=5, quantities=[1, 0, 1, 0, 2, 2])
    result = aoc202512.Region.from_string(region_str)
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input."""

    assert aoc202512.part1(*example1) == 2


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202512.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202512.part1(real_data) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_real(real_data):
    """Test part 2 on real input."""
    assert aoc202512.part2(real_data) == ...
