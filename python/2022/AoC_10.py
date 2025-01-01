from itertools import count


class CPU:
    def __init__(self, instructions: list[str], signals: tuple[int]) -> None:
        self.register = 1
        self.instructions = instructions
        self.signals = signals
        self.signal_strength = []
        self.display_buffer = []

    def run_program(self):
        pointer = 0
        cycle_count = 0
        for cycle in count(start=1):
            if not cycle_count:
                match self.instructions[pointer]:
                    case ["noop"]:
                        cycle_count = 1
                        number = 0
                    case ["addx", number]:
                        number = int(number)
                        cycle_count = 2
            cycle_count -= 1
            self.CRT_out(cycle)
            if cycle in self.signals:
                self.signal_strength.append(self.register * cycle)
            if not cycle_count:
                self.register += number
                pointer += 1
                if pointer >= len(self.instructions):
                    break

    def CRT_out(self, cycle):
        buffer_pos = (cycle - 1) % 40
        if abs(buffer_pos - self.register) < 2:
            self.display_buffer.append("#")
        else:
            self.display_buffer.append(" ")
        if buffer_pos == 39:
            print("".join(self.display_buffer))
            self.display_buffer.clear()

    def get_sum_signal_strength(self):
        return sum(self.signal_strength)


def read_file(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        return [tuple(line.split()) for line in lines]


if __name__ == "__main__":
    instructions = read_file("day10a_data")
    signals = (20, 60, 100, 140, 180, 220)
    my_CPU = CPU(instructions, signals)
    my_CPU.run_program()
    signal_strenth = my_CPU.get_sum_signal_strength()
    print(f"Part 1: {signal_strenth}")
