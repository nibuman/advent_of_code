import numpy as np
from itertools import product


class forest:
    def __init__(self, forest) -> None:
        self.forest = np.array(forest)
        self.visible_array = np.zeros(self.forest.shape).astype(bool)
        self.view_array = np.zeros(self.forest.shape).astype(int)
        self.HEIGHT, self.LENGTH = self.forest.shape
        self.tree_coordinates = list(product(range(self.HEIGHT), range(self.LENGTH)))

    def get_vis(self):
        for lane, visible_lane in zip(self.forest, self.visible_array):
            self.calc_visible(lane, visible_lane)
        for lane, visible_lane in zip(self.forest.T, self.visible_array.T):
            self.calc_visible(lane, visible_lane)

    def calc_visible(self, lane, visible_lane):
        """Return number of trees visible from each end"""
        left_vis = self._count_visible(lane.copy(), visible_lane)
        right_vis = self._count_visible(np.flip(lane.copy()), np.flip(visible_lane))
        return (left_vis, right_vis)

    def _count_visible(self, lane, visible_lane):
        clue = 0
        for idx in range(len(lane)):
            height = lane[idx]
            if height > 0 or (idx == 0):
                visible_lane[idx] = True
                clue += 1
                lane = lane - height
        return clue

    def visible_count(self):
        return np.sum(self.visible_array)

    def calc_viewing_distances(self):
        for idx_y, idx_x in self.tree_coordinates:
            left = self._measure_distance(idx_y, idx_x, lambda y, x: (y, x - 1))
            right = self._measure_distance(idx_y, idx_x, lambda y, x: (y, x + 1))
            up = self._measure_distance(idx_y, idx_x, lambda y, x: (y + 1, x))
            down = self._measure_distance(idx_y, idx_x, lambda y, x: (y - 1, x))
            self.view_array[idx_y, idx_x] = left * right * up * down
        return np.max(self.view_array)

    def _measure_distance(self, y, x, func):
        height = self.forest[y, x]
        distance = 0
        while (0 < y < self.HEIGHT - 1) and (0 < x < self.LENGTH - 1):
            distance += 1
            y, x = func(y, x)
            if self.forest[y, x] >= height:
                break
        return distance


def read_forest_file():
    with open("day8a_data", "r") as f:
        forest = f.read().strip().split("\n")
    return [[int(h) for h in lane] for lane in forest]


if __name__ == "__main__":
    this_forest = forest(read_forest_file())
    this_forest.get_vis()
    print("Part 1: ", this_forest.visible_count())
    print("Part 2: ", this_forest.calc_viewing_distances())
