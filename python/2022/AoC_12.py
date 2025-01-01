import numpy as np
from collections import deque


def BFS(elevation_map: np.array, start_pos: tuple[int], end_pos: tuple[int]) -> list:
    visited = set([start_pos])
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = deque([start_pos])
    level = {start_pos: 0}
    while queue:
        row, col = queue.popleft()
        if (row, col) == end_pos:
            return level
        current_height = ord(elevation_map[row, col])
        adjacent_positions = [
            (row + r, col + c)
            for r, c in moves
            if (0 <= row + r < HEIGHT) and (0 <= col + c < LENGTH)
        ]
        for pos in adjacent_positions:
            if (pos not in visited) and (
                (ord(elevation_map[pos]) - current_height) < 2
            ):
                visited.add(pos)
                queue.append(pos)
                level[pos] = level[(row, col)] + 1


def read_file(filename):
    with open(filename, "r") as f:
        return [list(line) for line in f.read().strip().split("\n")]


def get_replace_positions(my_map, initial, final):
    r, c = np.where(my_map == initial)
    my_map[my_map == initial] = final
    return (r[0], c[0])


if __name__ == "__main__":
    elevation_map = np.array(read_file("day12a_data"), dtype="U1")
    HEIGHT, LENGTH = elevation_map.shape
    start_pos = get_replace_positions(elevation_map, "S", "a")
    end_pos = get_replace_positions(elevation_map, "E", "z")
    distance = BFS(elevation_map, start_pos, end_pos)
    print("Dist: ", distance[end_pos])
    min_dist = distance[end_pos]
    a_pos = np.where(elevation_map == "a")
    a_pos = [(r, c) for r, c in zip(a_pos[0], a_pos[1])]
    for pos in a_pos:
        distance = BFS(elevation_map, pos, end_pos)
        if distance and distance[end_pos] < min_dist:
            min_dist = distance[end_pos]
    print(min_dist)
    pass
