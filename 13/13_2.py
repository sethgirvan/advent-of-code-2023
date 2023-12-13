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
        smudge_handled = False
        diff = np.logical_xor(rock_map[0], rock_map[i]).sum()
        if diff <= 1:
            if diff > 0:
                smudge_handled = True
            match = True
            for j in range(1, math.floor((i + 1) / 2)):
                diff = np.logical_xor(rock_map[j], rock_map[i - j]).sum()
                if not (diff == 0 or (diff == 1 and not smudge_handled)):
                    match = False
                    break
                if diff > 0:
                    smudge_handled = True
            if match and smudge_handled:
                return math.floor((i + 1) / 2)

    last = len(rock_map) - 1
    # Check for mirror matches containing bottom row
    for i in reversed(range(len(rock_map) % 2, len(rock_map) - 1, 2)):
        smudge_handled = False
        diff = np.logical_xor(rock_map[last], rock_map[i]).sum()
        if diff <= 1:
            if diff > 0:
                smudge_handled = True
            match = True
            for j in range(1, math.floor((last - i + 1) / 2)):
                diff = np.logical_xor(rock_map[i + j], rock_map[last - j]).sum()
                if not (diff == 0 or (diff == 1 and not smudge_handled)):
                   match = False
                   break
                if diff > 0:
                    smudge_handled = True
            if match and smudge_handled:
                return math.floor((i + last + 1) / 2)

    return 0

def rock_map_to_num(rock_map: NDArray) -> int:
    # Check for reflection across horizontal line
    horiz = horiz_mirror_row(rock_map)
    if horiz > 0:
        return 100 * horiz
    vert = horiz_mirror_row(rock_map.transpose())
    if vert > 0:
        return vert

    print("Failed for rock map")
    print(rock_map)
    return 0

rock_maps = get_maps()
# print([rock_map_to_num(rm) for rm in rock_maps])
print(sum(rock_map_to_num(rm) for rm in rock_maps))
