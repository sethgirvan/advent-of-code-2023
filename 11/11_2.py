import fileinput

map = [list(line.rstrip()) for line in fileinput.input()]

def row_is_empty(row: list[str]) -> bool:
    return all(c == "." for c in row)

def col_is_empty(col: int) -> bool:
    return all(row[col] == "." for row in map)

def insert_empty_col(col: int) -> None:
    for row in map:
        row.insert(col, ".")

# List of empty rows
empty_rows = [i for i, row in reversed(list(enumerate(map))) if row_is_empty(row)]

# List of empty columns
empty_cols = [j for j, _ in reversed(list(enumerate(map[0]))) if col_is_empty(j)]

print(f"empty_rows {empty_rows}")
print(f"empty_cols {empty_cols}")

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
        distance = abs(other[0] - galaxy[0]) + abs(other[1] - galaxy[1])
        top_row, bottom_row = sorted((galaxy[0], other[0]))
        left_col, right_col = sorted((galaxy[1], other[1]))
        # Do not need to include rows/cols containing the galaxies since they
        # cannot be empty.
        extra_row_dist = sum(999999 for row in range(top_row + 1, bottom_row) if row in empty_rows)
        extra_col_dist = sum(999999 for col in range(left_col + 1, right_col) if col in empty_cols)
        distances.append(distance + extra_row_dist + extra_col_dist)

print(distances)
print(len(distances))
print(sum(distances))
