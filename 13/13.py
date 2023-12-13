from collections.abc import Generator
from typing import Any
from numpy.typing import NDArray

import fileinput
import math
import numpy as np

def get_maps() -> Generator[NDArray, None, None]:
    rock_map: list[NDArray] = []
    for line in fileinput.input():
        stripped = line.rstrip()
        if stripped == "":
            yield np.array(rock_map)
            rock_map = []
        else:
            rock_map.append(np.array([True if c == "#" else False for c in stripped]))
    yield np.array(rock_map)

def horiz_mirror_row(rock_map: NDArray) -> int:
    # Check for mirror matches containing top row
    for i in range(1, len(rock_map), 2):
        if np.array_equal(rock_map[0], rock_map[i]):
            match = True
            for j in range(1, math.floor((i + 1) / 2)):
                if not np.array_equal(rock_map[j], rock_map[i - j]):
                    match = False
                    break
            if match:
                return math.floor((i + 1) / 2)

    last = len(rock_map) - 1
    # Check for mirror matches containing bottom row
    for i in reversed(range(0, len(rock_map) - 1)):
        if np.array_equal(rock_map[last], rock_map[i]):
            match = True
            for j in range(1, math.floor((last - i + 1) / 2)):
                if not np.array_equal(rock_map[i + j], rock_map[last - j]):
                    match = False
                    break
            if match:
                return math.floor((i + last + 1) / 2)

    return 0

def rock_map_to_num(rock_map: NDArray) -> int:
    # Check for reflection across horizontal line
    horiz = horiz_mirror_row(rock_map)
    if horiz > 0:
        return 100 * horiz
    else:
        return horiz_mirror_row(rock_map.transpose())

rock_maps = get_maps()
print(sum(rock_map_to_num(rm) for rm in rock_maps))
