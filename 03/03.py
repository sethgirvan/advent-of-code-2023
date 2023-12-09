import fileinput
import re

lines = [line.rstrip() for line in fileinput.input()]

sum = 0
for i, line in enumerate(lines):
    col = 0
    while True:
        print(f"line: {i}, col: {col}")
        # Note that match.start() and match.end() are relative to the substring
        # line[col:], so we need to add col to those values to get the actual
        # positions in the line.
        match = re.search(r"\d+", line[col:])
        if match is None:
            break

        min_col = col + match.start() - 1
        if min_col < 0:
            min_col = 0
        max_col = col + match.end() + 1
        if max_col > len(line):
            max_col = len(line)

        is_partnum = False

        start_row = i - 1
        if start_row < 0:
            start_row = 0
        end_row = i + 2
        if end_row > len(lines):
            end_row = len(lines)
        for check_line in lines[start_row:end_row]:
            if re.search(r"[^\d.]", check_line[min_col:max_col]) is not None:
                is_partnum = True
                break

        if is_partnum:
            val = int(match.group(0))
            print(f"line: {i}, col: {col}, val: {val} matches")
            sum += val

        col += match.end()

print(f"sum: {sum}")
