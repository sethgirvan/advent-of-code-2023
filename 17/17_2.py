from functools import total_ordering
from typing import Any

import fileinput
import heapq
import numpy as np
import numpy.typing as npt

@total_ordering
class toVisit:
    heat_loss: int
    direction: npt.NDArray
    forward_moves: int
    loc: npt.NDArray

    def __init__(
            self,
            heat_loss: int,
            direction: npt.NDArray,
            forward_moves: int,
            loc: npt.NDArray,
    ) -> None:
        self.heat_loss = heat_loss
        self.direction = direction
        self.forward_moves = forward_moves
        self.loc = loc

    def __lt__(self, other) -> bool:
        return self.heat_loss < other.heat_loss

def in_range(grid: list[list[Any]], idx: npt.NDArray) -> bool:
    i, j = idx
    return i >= 0 and i < len(grid) and j >= 0 and j < len(grid[i])

left = np.array([[0, 1], [-1, 0]])
right = np.array([[0, -1], [1, 0]])
grid = [[int(c) for c in line.rstrip()] for line in fileinput.input()]
visited: set[tuple[tuple[int, int], tuple[int, int], int]] = set()
heap: list[toVisit] = []

# Important to push both start directions here since for part two it will not
# immediately try turning due to minimum number of moves before turn.
heapq.heappush(heap, toVisit(0, np.array([0, 1]), 0, np.array([0, 0])))
heapq.heappush(heap, toVisit(0, np.array([1, 0]), 0, np.array([0,0])))

while len(heap) > 0:
    # print(len(heap))
    # print(f"len visited {len(visited)}")
    block = heapq.heappop(heap)
    i, j = block.loc
    if ((i, j), tuple(block.direction), block.forward_moves) in visited:
        continue # Already visited before

    visited.add(((i, j), tuple(block.direction), block.forward_moves))
    if i == len(grid) - 1 and j == len(grid[i]) - 1 and block.forward_moves >= 4:
        print(f"p2 answer: {block.heat_loss}")
        break

    if block.forward_moves >= 4:
        left_dir = np.matmul(left, block.direction)
        left_idx = block.loc + left_dir
        left_tup = tuple(left_idx)
        # print(f"left_idx {left_idx}")
        if in_range(grid, left_idx) and (left_tup, tuple(left_dir), 1) not in visited:
            left_heat_loss = grid[left_idx[0]][left_idx[1]]
            heapq.heappush(heap, toVisit(block.heat_loss + left_heat_loss, left_dir, 1, left_idx))

        right_dir = np.matmul(right, block.direction)
        right_idx = block.loc + right_dir
        right_tup = tuple(right_idx)
        # print(f"right_idx {right_idx}")
        if in_range(grid, right_idx) and (right_tup, tuple(right_dir), 1) not in visited:
            right_heat_loss = grid[right_idx[0]][right_idx[1]]
            heapq.heappush(heap, toVisit(block.heat_loss + right_heat_loss, right_dir, 1, right_idx))

    if block.forward_moves < 10:
        forward_idx = block.loc + block.direction
        forward_tup = tuple(forward_idx)
        # print(f"forward_idx {forward_idx}")
        if in_range(grid, forward_idx) and (forward_tup, tuple(block.direction), block.forward_moves + 1) not in visited:
            forward_heat_loss = grid[forward_idx[0]][forward_idx[1]]
            heapq.heappush(heap, toVisit(block.heat_loss + forward_heat_loss, block.direction, block.forward_moves + 1, forward_idx))
