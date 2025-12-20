"""Tests for AoC 9, 2025: Movie Theatre."""

# Third party imports
import aoc202509
import pytest
from aoc202509 import V


@pytest.fixture
def example1():
    puzzle_input = aoc202509.read_file("example1.txt")
    return aoc202509.parse(puzzle_input)


@pytest.fixture
def real_data():
    puzzle_input = aoc202509.read_file("input.txt")
    return aoc202509.parse(puzzle_input)


@pytest.mark.parametrize(
    ["v1", "v2", "expected_result"],
    [
        ((2, 2), (0, 1), 45),
        ((0, 1), (1, 0), 90),
        ((0, 1), (0, 1), 0),
    ],
)
def test_calculate_angle(v1, v2, expected_result):
    v1 = V.from_tuple(v1)
    v2 = V.from_tuple(v2)
    result = aoc202509.calculate_angle(v1, v2)
    assert expected_result == pytest.approx(result)


def test_convex_hull(example1):
    expected_result = [
        V(x=2, y=3),
        V(x=2, y=5),
        V(x=9, y=7),
        V(x=11, y=7),
        V(x=11, y=1),
        V(x=7, y=1),
    ]
    result = aoc202509.convex_hull(example1)
    assert all(expected == actual for expected, actual in zip(expected_result, result))


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202509.part1(example1) == 50


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202509.part2(example1) == ...


def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202509.part1(real_data) == 4735268538


@pytest.mark.skip(reason="Not implemented")
def test_part2_real(real_data):
    """Test part 2 on real input."""
    assert aoc202509.part2(real_data) == ...
