import fileinput
import re

def map_line_to_tuple(line: str) -> tuple[str, str, str]:
    nodes = re.findall(r"\w+", line)
    return (nodes[0], nodes[1], nodes[2])

with fileinput.input() as f:
    lines = iter(f)

    rl_ixs = next(lines).strip()

    next(lines) # Remove empty line
    tups = (map_line_to_tuple(l) for l in lines)
    map_dict = {t[0]: (t[1], t[2]) for t in tups}

    node = "AAA"
    step = 0
    while node != "ZZZ":
        print(node)
        ix = rl_ixs[step % len(rl_ixs)]
        print(ix)
        node = map_dict[node][0 if ix.upper() == "L" else 1]
        step += 1

print(step)
