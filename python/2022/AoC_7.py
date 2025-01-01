SIZE_LIMIT = 100000
total = 0
FILESYSTEM_SIZE = 70000000
SPACE_REQUIRED = 30000000
dir_summary = dict()


class directory:
    def __init__(self, name) -> None:
        self.name = name
        self.sub_directories = dict()
        self.files = dict()
        self.directory_size = 0

    def __repr__(self) -> str:
        return self.name


def parse(terminal_data):
    pwd = ["/"]
    file_tree = directory(pwd[0])
    current_directory = file_tree

    for line in terminal_data:
        match line.split():
            case ["$", "cd", "/"]:
                current_directory = file_tree
                pwd = ["/"]
            case ["$", "cd", ".."]:
                pwd.pop()
                current_directory = get_current_directory(file_tree, pwd)
            case ["$", "cd", directory_name]:
                if directory_name in current_directory.sub_directories:
                    pwd.append(directory_name)
                else:
                    current_directory.sub_directories[directory_name] = directory(
                        directory_name
                    )
                    pwd.append(directory_name)
                current_directory = get_current_directory(file_tree, pwd)
            case ["dir", _]:
                continue
            case ["$", "ls"]:
                continue
            case [file_size, file_name]:
                current_directory.files[file_name] = int(file_size)
            case _:
                assert False, "Something not right here..."
    sum_directories(file_tree)
    print("total = ", total)
    return file_tree


def get_file(filename):
    with open(filename, "r") as f:
        terminal_data = f.read().strip().split("\n")
    return terminal_data


def get_current_directory(filetree: directory, pwd: list[str]) -> directory:
    current_directory = filetree
    for directory in pwd:
        if directory == "/":
            continue
        current_directory = current_directory.sub_directories[directory]
    return current_directory


def sum_directories(this_directory: directory):
    global total
    global dir_summary
    this_directory.directory_size = sum(size for size in this_directory.files.values())
    for sub in this_directory.sub_directories.values():
        sum_directories(sub)
        this_directory.directory_size += sub.directory_size
    if this_directory.directory_size <= SIZE_LIMIT:
        print(f"{this_directory.name}, size={this_directory.directory_size}")
        total += this_directory.directory_size
    dir_summary[this_directory.name] = this_directory.directory_size


def find_directory_to_delete(used_space: int):
    SPACE_USED = used_space
    SPACE_REMAINING = FILESYSTEM_SIZE - SPACE_USED

    del_dir = min(
        dir_size
        for dir_size in dir_summary.values()
        if (SPACE_REMAINING + dir_size >= SPACE_REQUIRED)
    )
    print(
        "Dir size to delete = ",
        del_dir,
        "\n",
        SPACE_REMAINING,
        " + ",
        del_dir,
        " = ",
        SPACE_REMAINING + del_dir,
    )


if __name__ == "__main__":
    terminal_data = get_file("day7a_data")
    filetree = parse(terminal_data)
    find_directory_to_delete(filetree.directory_size)
