from collections import deque

MOVES = ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0))


def read_file(filename):
    with open(filename, "r") as f:
        return f.read().strip().split("\n")


def get_cubes(filename):
    cubes = dict()
    for cube in read_file(filename):
        x, y, z = cube.split(",")
        cubes[(int(x), int(y), int(z))] = 6
    return cubes


def bfs(lava_cubes: dict) -> list:
    cubes = {cube: 0 for cube in lava_cubes}
    x_min, *_, x_max = sorted(cube[0] for cube in cubes)
    y_min, *_, y_max = sorted(cube[1] for cube in cubes)
    z_min, *_, z_max = sorted(cube[2] for cube in cubes)
    start_pos = (x_min - 1, y_min - 1, z_min - 1)
    seen = set([start_pos])
    queue = deque([start_pos])
    while queue:
        x, y, z = queue.popleft()
        adjacent_positions = [
            (x + mx, y + my, z + mz)
            for mx, my, mz in MOVES
            if (x_min - 1 <= x <= x_max + 1)
            and (y_min - 1 <= y <= y_max + 1)
            and (z_min - 1 <= z <= z_max + 1)
        ]
        for pos in adjacent_positions:
            if pos in seen:
                continue
            elif pos in cubes:
                cubes[pos] += 1
            else:
                seen.add(pos)
                queue.append(pos)
    return cubes


if __name__ == "__main__":
    cubes = get_cubes("day18a_data")
    for x, y, z in cubes:
        for mx, my, mz in MOVES:
            adjacent_coordinates = (x + mx, y + my, z + mz)
            if adjacent_coordinates in cubes:
                cubes[(x, y, z)] -= 1
    print("Part 1: ", sum(cubes.values()))
    exposed_cubes = bfs(cubes)
    exposed_sides = sum(exposed_cubes.values())
    print("Part 2: ", exposed_sides)
