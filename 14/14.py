import fileinput

lines = [list(line.rstrip()) for line in fileinput.input()]

def roll_north(i: int, j: int) -> None:
    for dst in reversed(range(0, i)):
        if lines[dst][j] == ".":
            lines[dst][j] = "O"
            lines[dst + 1][j] = "."
        else:
            return

# Roll all 'O's as far north as they can go
for i in range(1, len(lines)):
    for j in range(0, len(lines[i])):
        if lines[i][j] == "O":
            roll_north(i, j)


for line in lines:
    print("".join(line))

p1 = sum((len(lines) - i) * count for i, count in enumerate(line.count("O") for line in lines))
print(f"p1 answer: {p1}")
