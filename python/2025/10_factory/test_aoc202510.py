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


@pytest.mark.parametrize(
    ["input", "expected_result"],
    [(".##.", 6), ("#..##", 25)],
)
def test_parse_lights(input: str, expected_result: int):
    result = aoc202510.Machine.parse_lights(input)
    assert result == expected_result


@pytest.mark.parametrize(
    ["input", "expected_result"],
    [
        ("(3) (1,3) (2) (2,3) (0,2) (0,1)", [8, 10, 4, 12, 5, 3]),
    ],
)
def test_parse_switches(input: str, expected_result: int):
    result = aoc202510.Machine.parse_switches(input)
    assert result == expected_result


@pytest.mark.parametrize(
    ["input", "expected_result"],
    [
        ([8, 10, 4], 6),
    ],
)
def test_press_switches(input: list[int], expected_result: int):
    result = aoc202510.press_switches(input)
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202510.part1(example1) == 7


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202510.part2(example1) == ...


def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202510.part1(real_data) == 530


@pytest.mark.skip(reason="Not implemented")
def test_part2_real(real_data):
    """Test part 2 on real input."""
    assert aoc202510.part2(real_data) == ...
