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


def get_line_positions(lines):
    filled_positions = set()
    for start, end in lines:
        start_x, end_x = sorted([start[0], end[0]])
        start_y, end_y = sorted([start[1], end[1]])
        if start_x == end_x:
            for y in range(start_y, end_y + 1):
                filled_positions.add((start_x, y))
        else:
            for x in range(start_x, end_x + 1):
                filled_positions.add((x, start_y))
    return filled_positions


def drop_sand(void_y: int, filled_positions: set):
    START_POS = pos = (500, 0)
    vectors = ((0, 1), (-1, 1), (1, 1))  # Directions sand can move in order of priority
    while (pos[1] < void_y) and (START_POS not in filled_positions):
        for v in vectors:
            # Can the sand move down into any of the allowed positions?
            if (new_pos := (pos[0] + v[0], pos[1] + v[1])) not in filled_positions:
                pos = new_pos
                break
        else:
            # Sand comes to rest and new sand drops from top
            filled_positions.add(pos)
            pos = START_POS
    return filled_positions


if __name__ == "__main__":
    path_list = read_file("day14a_data")
    lines = get_lines(path_list)
    max_y = max(line[0][1] for line in lines)
    filled_positions = get_line_positions(lines)
    start_filled_positions = len(filled_positions)
    end_filled_positions = len(drop_sand(max_y + 10, filled_positions))
    print("Part 1: ", end_filled_positions - start_filled_positions)
    X_LENGTH = 800
    for x in range(X_LENGTH):
        filled_positions.add((x, max_y + 2))
    start_filled_positions += X_LENGTH
    end_filled_positions = len(drop_sand(max_y + 10, filled_positions))
    print("Part 2: ", end_filled_positions - start_filled_positions)
