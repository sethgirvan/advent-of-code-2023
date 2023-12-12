import fileinput
import re

def count_arrangements(conditions: str, groups: list[int]) -> int:
    print(f"conditions {conditions} groups {groups}")
    if len(groups) == 0:
        return 0 if "#" in conditions else 1
    elif len(conditions) < 1:
        return 0

    arrangements = 0
    group = groups[0]
    group_sum = sum(groups)
    for i in range(0, len(conditions) - group_sum + 1):
        if conditions[i] == "#":
            return arrangements

        pattern = r"[.?][#?]{" + str(group) + r"}([.?]|$)"
        print(f"pattern {pattern}")
        match = re.match(pattern, conditions[i:])
        if match:
            print(f"match {match.group(0)}")
            offset = i + match.end()
            rest = "." + conditions[offset:]
            arrangements += count_arrangements(rest, groups[1:])
    return arrangements

pairs = (line.rstrip().split() for line in fileinput.input())
condition_rows, group_strs = zip(*pairs)
condition_rows_padded = ("." + c for c in condition_rows)
groups = ([int(x) for x in g.split(",")] for g in group_strs)
arrangement_counts = (count_arrangements(conditions, groups) for conditions, groups in zip(condition_rows_padded, groups))
answer = sum(arrangement_counts)
print(answer)
