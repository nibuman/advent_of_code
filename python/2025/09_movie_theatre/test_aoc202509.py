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
def example2():
    """See 2025-09_plans for shape"""
    points = [
        (2, 7),
        (2, 1),
        (5, 1),
        (5, 3),
        (7, 3),
        (7, 1),
        (11, 1),
        (11, 7),
        (26, 7),
        (26, 10),
        (11, 10),
        (11, 12),
        (9, 12),
        (9, 5),
        (7, 5),
        (7, 15),
        (2, 15),
        (2, 9),
        (4, 9),
        (4, 7),
    ]
    return [V(*point) for point in points]


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


def test_data_points_from_rect():
    rect = (V(2, 7), V(26, 10))
    expected_result = [V(2, 7), V(2, 10), V(26, 10), V(26, 7)]
    result = aoc202509.data_points_from_rect(rect)
    assert result == expected_result


@pytest.mark.parametrize(
    ["v_edge", "h_edge", "expected_result"],
    [
        ((V(3, 1), V(3, 5)), (V(1, 3), V(6, 3)), True),
        ((V(0, 1), V(0, 5)), (V(1, 3), V(6, 3)), False),
        ((V(3, 1), V(3, 3)), (V(1, 3), V(6, 3)), True),
    ],
)
def test_edges_intersect(v_edge, h_edge, expected_result):
    result = aoc202509.edges_intersect(v_edge=v_edge, h_edge=h_edge)
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


def test_part1_example2(example2):
    assert aoc202509.part1(example2) == 250


def test_part2_example2(example2):
    assert aoc202509.part2(example2) == 64


def test_get_lines(example2):
    assert aoc202509.get_edges(example2) == (
        [
            (V(x=2, y=2), V(x=2, y=6)),
            (V(x=5, y=2), V(x=5, y=2)),
            (V(x=7, y=2), V(x=7, y=2)),
            (V(x=11, y=2), V(x=11, y=6)),
            (V(x=26, y=8), V(x=26, y=9)),
            (V(x=11, y=11), V(x=11, y=11)),
            (V(x=9, y=6), V(x=9, y=11)),
            (V(x=7, y=6), V(x=7, y=14)),
            (V(x=2, y=10), V(x=2, y=14)),
            (V(x=4, y=8), V(x=4, y=8)),
        ],
        [
            (V(x=3, y=1), V(x=4, y=1)),
            (V(x=6, y=3), V(x=6, y=3)),
            (V(x=8, y=1), V(x=10, y=1)),
            (V(x=12, y=7), V(x=25, y=7)),
            (V(x=12, y=10), V(x=25, y=10)),
            (V(x=10, y=12), V(x=10, y=12)),
            (V(x=8, y=5), V(x=8, y=5)),
            (V(x=3, y=15), V(x=6, y=15)),
            (V(x=3, y=9), V(x=3, y=9)),
            (V(x=3, y=7), V(x=3, y=7)),
        ],
    )


def test_part2_real(real_data):
    """Test part 2 on real input.
    -    1737890 too low
    -    4595056840 too high
    -    4545260920 too high
    -    4541130976 ??
    -    116013455 ??
    """
    assert aoc202509.part2(real_data) == 1537458069
