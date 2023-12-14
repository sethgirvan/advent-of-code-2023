import copy
import fileinput

lines = [list(line.rstrip()) for line in fileinput.input()]

def roll_north(i: int, j: int) -> None:
    for dst in reversed(range(0, i)):
        if lines[dst][j] == ".":
            lines[dst][j] = "O"
            lines[dst + 1][j] = "."
        else:
            return

def roll_west(i: int, j: int) -> None:
    for dst in reversed(range(0, j)):
        if lines[i][dst] == ".":
            lines[i][dst] = "O"
            lines[i][dst + 1] = "."
        else:
            return

def roll_south(i: int, j: int) -> None:
    for dst in range(i + 1, len(lines)):
        if lines[dst][j] == ".":
            lines[dst][j] = "O"
            lines[dst - 1][j] = "."
        else:
            return

def roll_east(i: int, j: int) -> None:
    for dst in range(j + 1, len(lines[i])):
        if lines[i][dst] == ".":
            lines[i][dst] = "O"
            lines[i][dst - 1] = "."
        else:
            return

def spin_cycle() -> None:
    for i in range(1, len(lines)):
        for j in range(0, len(lines[i])):
            if lines[i][j] == "O":
                roll_north(i, j)
    for i in range(0, len(lines)):
        for j in range(1, len(lines[i])):
            if lines[i][j] == "O":
                roll_west(i, j)
    for i in reversed(range(0, len(lines) - 1)):
        for j in range(0, len(lines[i])):
            if lines[i][j] == "O":
                roll_south(i, j)
    for i in range(0, len(lines)):
        for j in reversed(range(0, len(lines[i]) - 1)):
            if lines[i][j] == "O":
                roll_east(i, j)

def tbls_cmp(a: list[list[str]], b: list[list[str]]) -> bool:
    for a_row, b_row in zip(a, b):
        for a_item, b_item in zip(a_row, b_row):
            if a_item != b_item:
                return False

    return True

def print_tbl(tbl: list[list[str]]) -> None:
    print("")
    for line in tbl:
        print("".join(line))

history: list[list[list[str]]] = []

def history_match(tbl: list[list[str]]) -> int:
    for j, h in enumerate(history):
        if tbls_cmp(h, lines):
            return j
    return -1

for i in range(1, 1000000001):
    history.append(copy.deepcopy(lines))
    print(f"spin cycle {i}")
    # cum = sum((len(lines) - i) * count for i, count in enumerate(line.count("O") for line in lines))
    # print(f"sum {cum}")
    spin_cycle()
    cycle_start = history_match(lines)
    if cycle_start >= 0:
        cycle_end = i
        break

print(f"cycle start {cycle_start} cycle end {cycle_end}")
cycle_len = cycle_end - cycle_start
idx = (1000000000 - cycle_start) % cycle_len + cycle_start

final = history[idx]
print_tbl(final)
p2 = sum((len(final) - i) * count for i, count in enumerate(line.count("O") for line in final))
print(f"p2 answer: {p2}")
