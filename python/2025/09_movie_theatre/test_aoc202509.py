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


@pytest.fixture
def example1_perimeter():
    return {
        V(x=11, y=1),
        V(x=11, y=7),
        V(x=2, y=4),
        V(x=4, y=3),
        V(x=7, y=3),
        V(x=9, y=5),
        V(x=11, y=2),
        V(x=6, y=3),
        V(x=11, y=5),
        V(x=2, y=5),
        V(x=3, y=5),
        V(x=5, y=5),
        V(x=7, y=1),
        V(x=6, y=5),
        V(x=8, y=1),
        V(x=9, y=6),
        V(x=11, y=3),
        V(x=10, y=1),
        V(x=10, y=7),
        V(x=11, y=6),
        V(x=2, y=3),
        V(x=8, y=5),
        V(x=4, y=5),
        V(x=3, y=3),
        V(x=7, y=2),
        V(x=5, y=3),
        V(x=7, y=5),
        V(x=9, y=1),
        V(x=9, y=7),
        V(x=11, y=4),
    }


@pytest.mark.parametrize(
    ["v1", "v2", "expected_result"],
    [
        ((2, 2), (0, 1), 45),
        ((0, 1), (1, 0), 90),
        ((0, 1), (0, 1), 0),
    ],
)
def test_calculate_angle(v1, v2, expected_result):
    v1 = V(*v1)
    v2 = V(*v2)
    result = aoc202509.calculate_angle(v1, v2)
    assert expected_result == pytest.approx(result)


def test_trace_perimeter(example1, example1_perimeter):
    expected_result = example1_perimeter
    result = aoc202509.trace_perimeter(example1)
    assert result == expected_result


def test_fill(example1_perimeter):
    expected_result = 46
    result = len(aoc202509.fill(perimeter=example1_perimeter))
    assert result == expected_result


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


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202509.part2(example1) == 24


def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202509.part1(real_data) == 4735268538


@pytest.mark.skip()
def test_part2_real(real_data):
    """Test part 2 on real input.
    -    1737890 too low
    -    4595056840 too high
    -    4545260920 too high
    -    4541130976 ??
    -    116013455 ??
    """
    assert aoc202509.part2(real_data) == ...
