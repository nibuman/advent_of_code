class vector:
    """Vector class that is hashable to allow use in sets.
    Addition and subtraction operators are overloaded
    """

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __sub__(self, other):
        return vector(self.row - other.row, self.col - other.col)

    def __add__(self, other):
        return vector(self.row + other.row, self.col + other.col)

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return (self.row == other.row) and (self.col == other.col)


vector_map = {
    "U": vector(1, 0),
    "D": vector(-1, 0),
    "L": vector(0, -1),
    "R": vector(0, 1),
}


def follow_instructions(directions: list[tuple[str, int]], rope_length: int) -> int:
    visited = set()
    knots = [vector(0, 0)] * rope_length
    visited.add(knots[-1])
    for direction, distance in directions:
        for _ in range(distance):
            # Move the head according to the directions
            knots[0] += vector_map[direction]
            # Go through each of the tail knots
            for idx in range(1, len(knots)):
                move_vector = _get_move_vector(knots[idx - 1], knots[idx])
                knots[idx] += move_vector
            visited.add(knots[-1])
    return len(visited)


def _get_move_vector(knot1: vector, knot2: vector) -> vector:
    """Returns the vector for moving the tail knots. Knots only move if
    they are not touching the knot infront."""
    diff_vector = knot1 - knot2
    move_map = {0: 0, 1: 1, -1: -1, 2: 1, -2: -1}
    if (abs(diff_vector.row) > 1) or (abs(diff_vector.col) > 1):
        return vector(move_map[diff_vector.row], move_map[diff_vector.col])
    else:
        return vector(0, 0)


def read_file(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    return [(line.split()[0], int(line.split()[1])) for line in lines]


if __name__ == "__main__":
    instructions = read_file("day9a_data")
    answer = follow_instructions(instructions, rope_length=2)
    print(f"Part 1: {answer}")
    answer = follow_instructions(instructions, rope_length=10)
    print(f"Part 2: {answer}")
