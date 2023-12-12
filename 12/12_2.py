import fileinput
import re

def arrangements_with_groups(conditions: str, groups: list[int]) -> list[int]:
    arrangements = [0 for _ in conditions]

    if len(groups) == 0:
        for i, _ in reversed(list(enumerate(conditions))):
            if conditions[i] == "#":
                return arrangements
            arrangements[i] = 1
        return arrangements

    group = groups[0]
    arrangements_rest = arrangements_with_groups(conditions, groups[1:])
    group_sum = sum(groups)
    section_cum = 0
    for i in reversed(range(0, len(conditions))):
        if conditions[i] == "#":
            section_cum = 0
        else:
            pattern = r"[.?][#?]{" + str(group) + r"}([.?])"
            # print(f"pattern {pattern}")
            match = re.match(pattern, conditions[i:])
            if match:
                # print(f"match {match.group(0)}")
                offset = i + match.end() - 1
                section_cum += arrangements_rest[offset]
        arrangements[i] = section_cum
    # print(f"groups {groups} arrangements {arrangements}")
    return arrangements

def count_arrangements(conditions: str, groups: list[int]) -> int:
    return arrangements_with_groups(conditions, groups)[0]

def expand_condition_row(conditions: str) -> str:
    return "?".join(conditions for _ in range(0, 5))

def expand_groups(groups: list[int]) -> list[int]:
    nested = (groups for _ in range(0, 5))
    return [g for sg in nested for g in sg]

pairs = (line.rstrip().split() for line in fileinput.input())
condition_rows, group_strs = zip(*pairs)
condition_rows_expanded = (expand_condition_row(c) for c in condition_rows)
condition_rows_padded = ("." + c + "." for c in condition_rows_expanded)
groups = ([int(x) for x in g.split(",")] for g in group_strs)
groups_expanded = (expand_groups(g) for g in groups)
arrangement_counts = (count_arrangements(conditions, groups) for conditions, groups in zip(condition_rows_padded, groups_expanded))
answer = sum(arrangement_counts)
print(answer)
