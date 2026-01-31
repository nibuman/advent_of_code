"""Tests for AoC 11, 2025: Reactor."""

# Third party imports
import aoc202511
import pytest


@pytest.fixture
def example1():
    puzzle_input = aoc202511.read_file("example1.txt")
    return aoc202511.parse(puzzle_input)


@pytest.fixture
def real_data():
    puzzle_input = aoc202511.read_file("input.txt")
    return aoc202511.parse(puzzle_input)


def test_parse_example1():
    """Test that input is parsed properly."""
    example1 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
    expected_result = {
        "aaa": ["you", "hhh"],
        "you": ["bbb", "ccc"],
        "bbb": ["ddd", "eee"],
        "ccc": ["ddd", "eee", "fff"],
        "ddd": ["ggg"],
        "eee": ["out"],
        "fff": ["out"],
        "ggg": ["out"],
        "hhh": ["ccc", "fff", "iii"],
        "iii": ["out"],
    }
    result = aoc202511.parse(example1)
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202511.part1(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202511.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part1_real(real_data):
    """Test part 1 on real input."""
    assert aoc202511.part1(real_data) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_real(real_data):
    """Test part 2 on real input."""
    assert aoc202511.part2(real_data) == ...
