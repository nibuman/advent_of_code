import itertools


def read_file(filename):
    with open(filename, "r") as f:
        return f.read().strip()


def format_item(buffer):
    if buffer.isdigit():
        item = int(buffer)
    else:
        item = buffer
    return item


def get_next_items(line):
    parentheses = 0
    items = []
    buffer = ""
    for char in line:
        if char == "[" and parentheses == 0:
            parentheses += 1
        elif char == "]" and parentheses == 1:
            items.append(format_item(buffer))
            buffer = ""
        elif char == "[":
            parentheses += 1
            buffer = f"{buffer}{char}"
        elif char == "]":
            buffer = f"{buffer}{char}"
            parentheses -= 1
        elif char == "," and parentheses == 1:
            items.append(format_item(buffer))
            buffer = ""
        else:
            buffer = f"{buffer}{char}"
    return items


def compare_lists(left, right):
    for l_item, r_item in itertools.zip_longest(left, right):
        while True:
            match [l_item, r_item]:
                case [int(l_num), int(r_num)]:
                    if r_num == l_num:
                        break
                    else:
                        return r_num > l_num
                case [None, rhs]:
                    if rhs is None:
                        break
                    else:
                        return True
                case [lhs, None]:
                    return False
                case [lhs, int(rhs)]:
                    lhs = get_next_items(lhs)
                    if (result := compare_lists(lhs, [rhs])) is None:
                        break
                    else:
                        return result
                case [int(lhs), rhs]:
                    rhs = get_next_items(rhs)
                    if (result := compare_lists([lhs], rhs)) is None:
                        break
                    else:
                        return result
                case [lhs, rhs]:
                    lhs = get_next_items(lhs)
                    rhs = get_next_items(rhs)
                    if (result := compare_lists(lhs, rhs)) is None:
                        break
                    else:
                        return result
                case _:
                    print("Ooops!")


if __name__ == "__main__":
    file = read_file("day13a_data")
    packets = file.split("\n\n")
    correct_indices = []
    for idx, packet in enumerate(packets, start=1):
        left, right = packet.split()
        left = get_next_items(left)
        right = get_next_items(right)
        if compare_lists(left, right):
            correct_indices.append(idx)
    print(f"Part 1: Sum of indices = {sum(correct_indices)}")

    packets = file.split("\n")
    packets.append("[[2]]")
    packets.append("[[6]]")
    packets = [p for p in packets if p != ""]

    changed = True
    while changed:
        changed = False
        for idx in range(len(packets) - 1):
            left = packets[idx]
            right = packets[idx + 1]
            lhs = get_next_items(left)
            rhs = get_next_items(right)
            if not compare_lists(lhs, rhs):
                packets[idx] = right
                packets[idx + 1] = left
                changed = True

    keys = []
    for idx, packet in enumerate(packets, start=1):
        if packet == "[[2]]" or packet == "[[6]]":
            keys.append(idx)
    print(f"Part 2: keys at {keys[0]} and {keys[1]}, product = {keys[0] * keys[1]}")
