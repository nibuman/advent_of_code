"""AoC 8, 2025: Playground."""

# Standard library imports
from dataclasses import dataclass, field
import pathlib
import sys
from datetime import datetime
import math
from typing import Generator
from itertools import combinations
from sklearn.neighbors import KDTree


@dataclass
class KD:
    dist: float
    idx: int

    @classmethod
    def from_query(
        cls, kd_tree: KDTree, data: list[tuple[int, int, int]], idx: int, k: int
    ) -> KD:
        dist, i = kd_tree.query(data[idx : idx + 1], k=k)
        return cls(dist=float(dist[0][-1]), idx=int(i[0][-1]))


@dataclass(unsafe_hash=True, eq=True)
class JunctionBox:
    x: int = field(hash=True, compare=True)
    y: int = field(hash=True, compare=True)
    z: int = field(hash=True, compare=True)
    k: int = field(hash=False, init=False, default=2, compare=False)
    attachments: list[JunctionBox] = field(
        default_factory=list, hash=False, init=False, compare=False
    )

    def __iter__(self) -> Generator[int, None, None]:
        yield self.x
        yield self.y
        yield self.z

    def __sub__(self, other) -> float:
        return math.dist(self, other)

    def __str__(self):
        return f"x, y, z = {self.x}, {self.y}, {self.z}"

    def as_tuple(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)


def parse(puzzle_input: str) -> list[JunctionBox]:
    """Parse input."""
    rows = puzzle_input.split("\n")
    return [JunctionBox(*[int(num) for num in row.split(",")]) for row in rows]


def dbg_jbpairs(jb_pairs):
    print(
        "".join(f"{jb1}  -  {jb2}  (dist={jb1 - jb2})\n" for jb1, jb2 in jb_pairs[:5])
    )


def part1_kdtree(data: list[JunctionBox], data_set: str):
    """Solve part 1."""
    jb_pairs: list[tuple[JunctionBox, JunctionBox]] = []
    jb_init: list[tuple[JunctionBox, JunctionBox]] = []
    pair_length = {"example1": 10, "input": 1000}[data_set]
    kd_data = [jb.as_tuple() for jb in data]
    kd_tree = KDTree(kd_data, leaf_size=2, metric="euclidean")
    for i, jb in enumerate(data):
        while True:
            nearest = KD.from_query(kd_tree=kd_tree, data=kd_data, idx=i, k=jb.k)
            idx1 = min([i, nearest.idx])
            idx2 = max([i, nearest.idx])
            pair = (data[idx1], data[idx2])
            jb.k += 1
            if pair in jb_init and jb.k < len(data):
                continue
            jb_init.append(pair)
            break
    for _ in range(pair_length):
        closest_pair = min(jb_init, key=lambda x: x[0] - x[1])
        jb_pairs.append(closest_pair)
        jb_init.remove(closest_pair)
        jbs_in_jb_init = {pair[0] for pair in jb_init}
        missing = [(i, jb) for i, jb in enumerate(data) if jb not in jbs_in_jb_init]
        for i, jb in missing:
            while True:
                nearest = KD.from_query(kd_tree=kd_tree, data=kd_data, idx=i, k=jb.k)
                idx1 = min([i, nearest.idx])
                idx2 = max([i, nearest.idx])
                pair = (data[idx1], data[idx2])
                jb.k += 1
                if pair in jb_init and jb.k < len(data):
                    continue
                jb_init.append(pair)
                break

    # breakpoint()

    jb_pairs.sort(key=lambda x: x[0] - x[1])
    dbg_jbpairs(jb_pairs=jb_pairs)

    jbs = set()
    for first_jb, second_jb in jb_pairs[:pair_length]:
        first_jb.attachments.append(second_jb)
        second_jb.attachments.append(first_jb)
        jbs.update((first_jb, second_jb))

    path_lengths = []
    while jbs:
        jb = jbs.pop()
        jbs.add(jb)
        path_lengths.append(get_path_len(jb, jbs))
    return math.prod(sorted(path_lengths, reverse=True)[0:3])


def part1(data: list[JunctionBox], data_set: str):
    """Solve part 1."""
    pair_length = {"example1": 10, "input": 1000}[data_set]
    jb_pairs = sorted(list(combinations(data, 2)), key=lambda x: x[0] - x[1])
    jbs = set()
    dbg_jbpairs(jb_pairs=jb_pairs)
    for first_jb, second_jb in jb_pairs[:pair_length]:
        first_jb.attachments.append(second_jb)
        second_jb.attachments.append(first_jb)
        jbs.update((first_jb, second_jb))

    path_lengths = []
    while jbs:
        jb = jbs.pop()
        jbs.add(jb)
        path_lengths.append(get_path_len(jb, jbs))
    return math.prod(sorted(path_lengths, reverse=True)[0:3])


def get_path_len(jb: JunctionBox, jbs: set) -> int:
    if jb not in jbs:
        return 0
    jbs.discard(jb)
    path_len = 1
    for next_jb in jb.attachments:
        path_len += get_path_len(next_jb, jbs)
    return path_len


def part2(data: list[JunctionBox], data_set: str):
    """Solve part 2."""

    jb_pairs = sorted(list(combinations(data, 2)), key=lambda x: x[0] - x[1])
    jbs = set()
    for first_jb, second_jb in jb_pairs:
        first_jb.attachments.append(second_jb)
        second_jb.attachments.append(first_jb)
        jbs.update((first_jb, second_jb))
        if get_path_len(jb_pairs[-1][0], jbs.copy()) == len(data):
            return first_jb.x * second_jb.x


def solve(puzzle_input, data_set: str):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    for name, func in (
        ("Part1", part1),
        ("Part1 kdtree", part1_kdtree),
        # ("Part2", part2),
    ):
        t1 = datetime.now()
        result = func(data, data_set)
        t2 = datetime.now()
        data = parse(puzzle_input)
        yield name, result, (t2 - t1).microseconds


def read_file(file_name) -> str:
    PUZZLE_DIR = pathlib.Path(__file__).parent
    return pathlib.Path(PUZZLE_DIR / file_name).read_text().rstrip()


if __name__ == "__main__":
    DEFAULT_INPUT_FILES = ["example1.txt", "input.txt"]
    puzzle_input_files = sys.argv[1:] or DEFAULT_INPUT_FILES
    for file_name in puzzle_input_files:
        print(f"\n{file_name}:")
        solutions = solve(
            puzzle_input=read_file(file_name), data_set=file_name.removesuffix(".txt")
        )
        print(
            "\n".join(
                f"{puzzle}: {solution} (in {time / 1000} ms)"
                for puzzle, solution, time in solutions
            )
        )
