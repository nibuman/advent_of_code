"""
AoC 2022 Day 15

Tried this 3 ways:
a) For each sensor, search along the relevant line to see which positions were within
the Manhattan distance of each sensor
b) Calculate where the manhattan distance for each sensor intersects the given line,
then create a set() of all the positions between the 2 intersects
c) Calculate where the manhattan distance for each sensor intersects the given line,
represent the line as a 1D numpy array of False, and set those values to True

Part 1a: 5838453 in 21.411998896001023s using search
Part 1b: 5838453 in 0.8028492820012616s using calculation, tracking using set()
Part 1c: 5838453 in 0.001331638002739055s using calculation, tracking using numpy array

"""


import re
import time
import numpy as np


PART1_LINE_NUMBER = 2_000_000
no_beacons = set()
beacons = set()


def read_file(filename):
    with open(filename, "r") as f:
        return f.read().strip().split("\n")


def manhattan_distance(point_A, point_B) -> int:
    x_vector = abs(point_B[0] - point_A[0])
    y_vector = abs(point_B[1] - point_A[1])
    return x_vector + y_vector


def intersection(line_number, sensor):
    x, y, md = sensor
    delta_y = abs(y - line_number)
    delta_x = md - delta_y
    if delta_x < 0:
        return None
    return (x - delta_x, x + delta_x)


def get_all_intersections(line_number):
    intersections = []
    for sensor in sensors:
        if this_intersection := intersection(line_number, sensor):
            intersections.append(this_intersection)
    return intersections


if __name__ == "__main__":
    beacon_sensor_list = read_file("day15a_data")
    sensors = []
    for line in beacon_sensor_list:
        match = re.search(
            r"\ASensor at x=(?P<sensor_x>-*\d+), y=(?P<sensor_y>-*\d+): closest beacon "
            r"is at x=(?P<beacon_x>-*\d+), y=(?P<beacon_y>-*\d+)\Z",
            line,
        )
        sensor_x = int(match["sensor_x"])
        sensor_y = int(match["sensor_y"])
        beacon_x = int(match["beacon_x"])
        beacon_y = int(match["beacon_y"])

        md = manhattan_distance((sensor_x, sensor_y), (beacon_x, beacon_y))
        sensors.append((sensor_x, sensor_y, md))
        beacons.add((beacon_x, beacon_y))

    t1 = time.perf_counter()
    intersections = get_all_intersections(PART1_LINE_NUMBER)
    min_x = min(intersections, key=lambda x: x[0])[0]
    max_x = max(intersections, key=lambda x: x[1])[1]
    offset = 0 if min_x >= 0 else abs(min_x)
    array_length = max_x + offset + 1
    line_array = np.zeros(array_length, dtype=bool)
    for start_x, end_x in intersections:
        line_array[start_x + offset : end_x + offset + 1] = True
    for beacon in beacons:
        if beacon[1] == PART1_LINE_NUMBER:
            line_array[beacon[1] + offset] = False
    t2 = time.perf_counter()

    print(
        f"Part 1c: {np.sum(line_array)} in {t2-t1}s using calculation, tracking using numpy array (bool)"
    )
    t3 = time.perf_counter()
    ARRAY_SIZE = 4_000_000
    PRINT_STEP = 10_000
    line_array = np.zeros(ARRAY_SIZE, dtype=bool)
    prev_time = t3
    for row in range(ARRAY_SIZE):

        if row % PRINT_STEP == 0:
            current_time = time.perf_counter()
            print(f"Progress {row} {100 * row / ARRAY_SIZE}%  in {current_time - t3}")
        intersections = get_all_intersections(row)
        for min_x, max_x in intersections:
            if min_x < 0:
                min_x = 0
            line_array[min_x : max_x + 1] = True
        if not np.all(line_array):
            for x_pos, is_not_beacon in enumerate(line_array):
                if not is_not_beacon:
                    x_mult = 4_000_000
                    t4 = time.perf_counter()
                    print(
                        f"Part 2: x={x_pos}, y={row}, frequency={(x_pos * x_mult)+ row} in {t4-t3}s"
                    )
                    exit()
        line_array.fill(False)
