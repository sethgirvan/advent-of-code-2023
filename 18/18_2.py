import fileinput

def add_tuples(t1, t2) -> tuple[int, int]:
    return tuple(i1 + i2 for i1, i2 in zip(t1, t2))

def dir_to_step(direction: str, dist: int) -> tuple[int, int]:
    match direction:
        case "R":
            return (0, dist)
        case "U":
            return (-dist, 0)
        case "L":
            return (0, -dist)
        case "D":
            return (dist, 0)
    raise Exception(f"Unexpected direction '{direction}'")

digit_to_dir = ["R", "D", "L", "U"]

def hex_to_ix(hexcode: str) -> tuple[str, int]:
    """
    Returns tuple (direction, distance)
    """
    return (digit_to_dir[int(hexcode[-2:-1])], int(hexcode[2:7], base=16))

ix_strs = (line.split() for line in fileinput.input())
ixs = (hex_to_ix(ix[2]) for ix in ix_strs)

steps = 0
integral = 0
pos = (0, 0)

for ix in ixs:
    direction, dist = ix
    steps += dist
    step = dir_to_step(direction, dist)
    integral -= step[1] * pos[0]
    pos = add_tuples(pos, step)

print(f"steps {steps}")
# area = abs(integral)
# Area internal to the path = area - steps/2 + 1 by Pick's theorem
# (https://en.wikipedia.org/wiki/Pick%27s_theorem)
# Total area is then the outer path area (just steps) plus that internal area.
p2 = steps + abs(integral) - int(steps/2) + 1
print(f"Part 2 answer: {p2}")
