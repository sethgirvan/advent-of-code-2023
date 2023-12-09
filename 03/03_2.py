from typing import List
import fileinput
import re

def all_gear_ratios(line: str, min_col: int, max_col: int) -> List[int]:
    ratios: List[int] = []
    col = 0
    while True:
        match = re.search(r"\d+", line[col:])
        if match is None:
            break
        match_start_col = col + match.start()
        match_end_col = col + match.end()
        # check for overlap of ranges
        if max(min_col, match_start_col) < min(max_col, match_end_col):
            ratios.append(int(match.group(0)))
        col += match.end()
    return ratios

lines = [line.rstrip() for line in fileinput.input()]

sum = 0
for i, line in enumerate(lines):
    col = 0
    while True:
        print(f"line: {i}, col: {col}")
        # Note that match.start() and match.end() are relative to the substring
        # line[col:], so we need to add col to those values to get the actual
        # positions in the line.
        match = re.search(r"\*", line[col:])
        if match is None:
            break

        min_col = col + match.start() - 1
        if min_col < 0:
            min_col = 0
        max_col = col + match.end() + 1
        if max_col > len(line):
            max_col = len(line)

        gear_ratios: List[int] = []

        start_row = i - 1
        if start_row < 0:
            start_row = 0
        end_row = i + 2
        if end_row > len(lines):
            end_row = len(lines)
        for check_line in lines[start_row:end_row]:
            gear_ratios += all_gear_ratios(check_line, min_col, max_col)

        if len(gear_ratios) == 2:
            print(f"line: {i}, col: {col + match.start()}, {gear_ratios[0]} and {gear_ratios[1]} matches")
            sum += gear_ratios[0] * gear_ratios[1]

        col += match.end()

print(f"sum: {sum}")
