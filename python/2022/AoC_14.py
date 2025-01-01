import numpy as np


class vector:
    """Vector class that is hashable to allow use in sets.
    Addition and subtraction operators are overloaded
    """

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def as_tuple(self):
        return (self.row, self.col)

    def __sub__(self, other):
        return vector(self.row - other.row, self.col - other.col)

    def __add__(self, other):
        return vector(self.row + other.row, self.col + other.col)

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return (self.row == other.row) and (self.col == other.col)


def read_file(filename):
    with open(filename, "r") as f:
        return f.read().strip().split("\n")


def get_lines(path_list):
    lines = []
    for paths in path_list:
        buffer = []
        for path in paths.split(" -> "):
            buffer.insert(0, path)
            if len(buffer) > 1:
                lines.append((buffer.pop().split(","), (buffer[0].split(","))))
    return [
        ((int(line[0][0]), int(line[0][1])), (int(line[1][0]), int(line[1][1])))
        for line in lines
    ]


def draw_lines(grid: np.array, lines):
    for start, end in lines:
        start_y = min(start[1], end[1])
        start_x = min(start[0], end[0])
        end_y = max(start[1], end[1]) + 1
        end_x = max(start[0], end[0]) + 1
        grid[start_y:end_y, start_x:end_x] = "#"


def drop_sand(grid: np.array, void_y: int):
    vector_map = dict(d=vector(1, 0), dl=vector(1, -1), dr=vector(1, 1))
    START_POS = vector(0, 500)
    sand_pos = START_POS
    while sand_pos.row < void_y:
        grid[sand_pos.as_tuple()] = "O"
        if grid[(sand_pos + vector_map["d"]).as_tuple()] == ".":
            move_vector = vector_map["d"]
        elif grid[(sand_pos + vector_map["dl"]).as_tuple()] == ".":
            move_vector = vector_map["dl"]
        elif grid[(sand_pos + vector_map["dr"]).as_tuple()] == ".":
            move_vector = vector_map["dr"]
        else:
            sand_pos = START_POS
            if grid[START_POS.as_tuple()] == "O":
                break
            continue
        grid[sand_pos.as_tuple()] = "."
        sand_pos = sand_pos + move_vector
    return np.sum(grid == "O")


if __name__ == "__main__":
    path_list = read_file("day14a_data")
    lines = get_lines(path_list)
    max_x = max(line[0][0] for line in lines)
    max_y = max(line[0][1] for line in lines)
    grid = np.empty((max_y + 10, max_x + 1000), dtype="U1")
    grid.fill(".")
    draw_lines(grid, lines)
    window = grid[0:10, 494:504]
    sand_count = drop_sand(grid, max_y + 4)
    print("Part 1: ", sand_count)
    grid[max_y + 2 : max_y + 3, :] = "#"
    sand_count = drop_sand(grid, max_y + 5)
    window = grid[0:13, 492:510]
    print("Part 2: ", sand_count)
    pass
