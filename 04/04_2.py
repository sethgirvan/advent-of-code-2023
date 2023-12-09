import fileinput
import re

card_counts = [1 for _ in fileinput.input()]
for i, line in enumerate(fileinput.input()):
    match = re.match(r"^Card +\d+: +([^|]*) *\| *(.*)$", line)
    if match is None:
        raise Exception("No match found")
    winning_group = match.group(1)
    our_group = match.group(2)

    winning_set = {num for num in re.findall(r"\d+", winning_group)}
    our = re.findall(r"\d+", our_group)
    winning_count = sum(x in winning_set for x in our)
    print(f"Winning number match count: {winning_count}")
    for j in range(1, winning_count + 1):
        card_counts[i + j] += card_counts[i]

total = sum(card_counts)
print(f"Total: {total}")
