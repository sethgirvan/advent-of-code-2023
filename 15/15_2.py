import fileinput
import re

boxes: list[list[tuple[str, int]]] = [[] for _ in range(0, 256)]

line = next(fileinput.input()).rstrip()

def hash_str(input: str) -> int:
    hash = 0
    for c in input:
        hash = 17 * (hash + ord(c)) % 256
    return hash

def find_label(box: list[tuple[str, int]], label: str) -> int:
    for i, lens in enumerate(box):
        if lens[0] == label:
            return i
    return -1

def box_sum(box: list[tuple[str, int]]) -> int:
    return sum((i + 1) * lens[1] for i, lens in enumerate(box))

for step in line.split(","):
    match = re.match(r"([a-z]+)([=-])(\d*)", step)
    label = match.group(1)
    label_hash = hash_str(label)
    box = boxes[label_hash]
    op = match.group(2)
    # print(f"label {label} op {op}")
    idx = find_label(box, label)

    if op == "=":
        focal = int(match.group(3))
        if idx >= 0:
            box[idx] = (label, focal)
        else:
            box.append((label, focal))
    else: # op == "-"
        idx = find_label(box, label)
        if idx >= 0:
            del box[idx]

p2 = sum((i + 1) * box_sum(box) for i, box in enumerate(boxes))
print(f"p2 answer: {p2}")
