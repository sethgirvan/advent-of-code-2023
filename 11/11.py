import fileinput

map = [list(line.rstrip()) for line in fileinput.input()]

def row_is_empty(row: list[str]) -> bool:
    return all(c == "." for c in row)

def col_is_empty(col: int) -> bool:
    return all(row[col] == "." for row in map)

def insert_empty_col(col: int) -> None:
    for row in map:
        row.insert(col, ".")

# Add extra empty rows
for i, row in reversed(list(enumerate(map))):
    if row_is_empty(row):
        map.insert(i, row)

# Add extra empty columns
for j, _ in reversed(list(enumerate(map[0]))):
    if col_is_empty(j):
        insert_empty_col(j)

# Print expanded map
for line in map:
    print("".join(line))

# Build list of all galaxy locations (row, col)
galaxies: list[tuple[int, int]] = []
for i, row in enumerate(map):
    for j, c in enumerate(row):
        if c == "#":
            galaxies.append((i, j))

# Build list of distances
distances: list[int] = []
for i, galaxy in enumerate(galaxies):
    for j in range(i + 1, len(galaxies)):
        other = galaxies[j]
        distances.append(abs(other[0] - galaxy[0]) + abs(other[1] - galaxy[1]))

print(distances)
print(len(distances))
print(sum(distances))
