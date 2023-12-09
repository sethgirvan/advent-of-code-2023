import fileinput
import re

total = 0
for line in fileinput.input():
    match = re.match(r"^Card +\d+: +([^|]*) *\| *(.*)$", line)
    if match is None:
        raise Exception("No match found")
    winning_group = match.group(1)
    our_group = match.group(2)

    winning_set = {num for num in re.findall(r"\d+", winning_group)}
    our = re.findall(r"\d+", our_group)
    winning_count = sum(x in winning_set for x in our)
    print(f"Winning number match count: {winning_count}")
    if winning_count > 0:
        total += 2**(winning_count - 1)

print(f"Total: {total}")
