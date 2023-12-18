from collections import deque
from typing import Any

import fileinput

RIGHT = 1
UP = 1 << 1
LEFT = 1 << 2
DOWN = 1 << 3

directions = [RIGHT, UP, LEFT, DOWN]

dir_to_step: dict[int, tuple[int, int]] = {
        RIGHT: (0, 1),
        UP: (-1, 0),
        LEFT: (0, -1),
        DOWN: (1, 0),
}

next_dir: dict[tuple[str, int], int] = {
        (".", RIGHT): RIGHT,
        (".", UP): UP,
        (".", LEFT): LEFT,
        (".", DOWN): DOWN,
        ("/", RIGHT): UP,
        ("/", UP): RIGHT,
        ("/", LEFT): DOWN,
        ("/", DOWN): LEFT,
        ("\\", RIGHT): DOWN,
        ("\\", UP): LEFT,
        ("\\", LEFT): UP,
        ("\\", DOWN): RIGHT,
        ("|", RIGHT): UP | DOWN,
        ("|", UP): UP,
        ("|", LEFT): UP | DOWN,
        ("|", DOWN): DOWN,
        ("-", RIGHT): RIGHT,
        ("-", UP): LEFT | RIGHT,
        ("-", LEFT): LEFT,
        ("-", DOWN): LEFT | RIGHT,
}

def add_tuples(t1, t2) -> tuple[int, int]:
    return tuple(i1 + i2 for i1, i2 in zip(t1, t2))

def in_range(grid: list[list[Any]], idx: tuple[int, int]) -> bool:
    i, j = idx
    return i >= 0 and i < len(grid) and j >= 0 and j < len(grid[i])

class gridSquare:
    character: str
    beam_dirs: int

    def __init__(self, character: str) -> None:
        self.character = character
        self.beam_dirs = 0

    def __str__(self) -> str:
        if self.beam_dirs == 0:
            return self.character
        else:
            return "#"

    def next_dirs(self, direction: int) -> int:
        return next_dir[(self.character, direction)]

def print_grid(grid: list[list[gridSquare]]) -> None:
    for line in grid:
        print("".join(str(square) for square in line))

grid = [[gridSquare(c) for c in line.rstrip()] for line in fileinput.input()]
bfs_queue: deque[tuple[tuple[int, int], int]] = deque([((0, 0), RIGHT)])
squares_energized_cnt = 0
while len(bfs_queue) > 0:
    (i, j), direction = bfs_queue.pop()
    square = grid[i][j]
    if square.beam_dirs & direction:
        # This square has already been visited in this direction: we are in are
        # loop so should stop following this path.
        continue
    if square.beam_dirs == 0:
        squares_energized_cnt += 1
    square.beam_dirs |= direction

    next_dirs = square.next_dirs(direction)
    for d in directions:
        if next_dirs & d:
            step = dir_to_step[d]
            next_square = add_tuples((i, j), step)
            if in_range(grid, next_square):
                bfs_queue.append((next_square, d))
print_grid(grid)
print(f"p1 answer {squares_energized_cnt}")
